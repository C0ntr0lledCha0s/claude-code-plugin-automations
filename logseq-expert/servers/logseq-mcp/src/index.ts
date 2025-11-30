#!/usr/bin/env node
/**
 * Logseq MCP Server
 *
 * Model Context Protocol server for Logseq integration.
 * Provides tools and resources for interacting with Logseq graphs.
 *
 * Environment variables:
 *   LOGSEQ_API_TOKEN (required): Authorization token from Logseq
 *   LOGSEQ_API_URL: Full URL (e.g., "http://192.168.1.100:45454")
 *   LOGSEQ_API_HOST: Host address (default: "127.0.0.1")
 *   LOGSEQ_API_PORT: Port number (default: "12315")
 *
 * Usage:
 *   LOGSEQ_API_TOKEN=xxx npx logseq-mcp
 *   LOGSEQ_API_TOKEN=xxx LOGSEQ_API_URL=http://192.168.1.100:45454 npx logseq-mcp
 *   LOGSEQ_API_TOKEN=xxx LOGSEQ_API_HOST=192.168.1.100 LOGSEQ_API_PORT=45454 npx logseq-mcp
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListResourceTemplatesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import { LogseqHttpClient, createClientFromEnv, getConfiguredUrl } from "./client/logseq-http.js";
import { readTools, handleReadTool } from "./tools/read-tools.js";
import { writeTools, handleWriteTool } from "./tools/write-tools.js";
import { queryTools, handleQueryTool } from "./tools/query-tools.js";
import {
  getResourceTemplates,
  listResources,
  readResource,
} from "./resources/graph-resources.js";

// Server metadata
const SERVER_NAME = "logseq-mcp";
const SERVER_VERSION = "1.0.0";

// All available tools
const allTools = [...readTools, ...writeTools, ...queryTools];

// Tool name to handler mapping
const toolHandlers: Record<
  string,
  (client: LogseqHttpClient, args: Record<string, unknown>) => Promise<unknown>
> = {};

// Register read tools
for (const tool of readTools) {
  toolHandlers[tool.name] = (client, args) => handleReadTool(client, tool.name, args);
}

// Register write tools
for (const tool of writeTools) {
  toolHandlers[tool.name] = (client, args) => handleWriteTool(client, tool.name, args);
}

// Register query tools
for (const tool of queryTools) {
  toolHandlers[tool.name] = (client, args) => handleQueryTool(client, tool.name, args);
}

/**
 * Create and start the MCP server
 */
async function main(): Promise<void> {
  // Create Logseq client from environment
  let client: LogseqHttpClient;
  try {
    client = createClientFromEnv();
  } catch (error) {
    console.error(
      "Failed to create Logseq client. Make sure LOGSEQ_API_TOKEN is set."
    );
    console.error(error instanceof Error ? error.message : String(error));
    process.exit(1);
  }

  // Test connection
  const connected = await client.testConnection();
  if (!connected) {
    console.error(
      "Cannot connect to Logseq. Make sure Logseq is running with HTTP API enabled."
    );
    console.error(`Trying to connect to: ${getConfiguredUrl()}`);
    process.exit(1);
  }

  // Create MCP server
  const server = new Server(
    {
      name: SERVER_NAME,
      version: SERVER_VERSION,
    },
    {
      capabilities: {
        tools: {},
        resources: {},
      },
    }
  );

  // Handle tool listing
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools: allTools };
  });

  // Handle tool execution
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    const handler = toolHandlers[name];
    if (!handler) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Unknown tool: ${name}` }),
          },
        ],
        isError: true,
      };
    }

    try {
      const result = await handler(client, (args ?? {}) as Record<string, unknown>);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: error instanceof Error ? error.message : String(error),
            }),
          },
        ],
        isError: true,
      };
    }
  });

  // Handle resource template listing
  server.setRequestHandler(ListResourceTemplatesRequestSchema, async () => {
    return { resourceTemplates: getResourceTemplates() };
  });

  // Handle resource listing
  server.setRequestHandler(ListResourcesRequestSchema, async () => {
    const resources = await listResources(client);
    return { resources };
  });

  // Handle resource reading
  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const { uri } = request.params;

    try {
      return await readResource(client, uri);
    } catch (error) {
      return {
        contents: [
          {
            uri,
            mimeType: "application/json",
            text: JSON.stringify({
              error: error instanceof Error ? error.message : String(error),
            }),
          },
        ],
      };
    }
  });

  // Start server with stdio transport
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Log startup (to stderr so it doesn't interfere with MCP protocol)
  console.error(`${SERVER_NAME} v${SERVER_VERSION} started`);
  console.error(`Connected to Logseq at ${getConfiguredUrl()}`);
}

// Run the server
main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
