/**
 * Logseq HTTP API Client
 *
 * Provides a typed interface to the Logseq HTTP API.
 */

export interface LogseqConfig {
  url: string;
  token: string;
}

export interface Page {
  uuid: string;
  name: string;
  "original-name"?: string;
  properties?: Record<string, unknown>;
  "journal?"?: boolean;
}

export interface Block {
  uuid: string;
  content: string;
  page?: { id: number; name?: string };
  parent?: { id: number };
  left?: { id: number };
  children?: Block[];
  properties?: Record<string, unknown>;
  "pre-block?"?: boolean;
}

export interface SearchResult {
  uuid: string;
  content: string;
  page: string;
}

export class LogseqHttpError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public response?: unknown
  ) {
    super(message);
    this.name = "LogseqHttpError";
  }
}

export class LogseqHttpClient {
  private url: string;
  private token: string;

  constructor(config: LogseqConfig) {
    this.url = config.url.replace(/\/$/, "");
    this.token = config.token;
  }

  /**
   * Make an API call to Logseq
   */
  private async call<T>(method: string, args: unknown[] = []): Promise<T> {
    const response = await fetch(`${this.url}/api`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`,
      },
      body: JSON.stringify({ method, args }),
    });

    if (!response.ok) {
      // Try to get error details from response body
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      try {
        const errorData = await response.json() as Record<string, unknown>;
        if (errorData.error || errorData.message) {
          errorMessage = String(errorData.error || errorData.message);
        }
      } catch {
        // Ignore JSON parsing errors for error responses
      }
      throw new LogseqHttpError(errorMessage, response.status);
    }

    // Logseq API returns data directly, not wrapped in {result: ...}
    const data = await response.json();

    // Handle error responses that come with 200 status
    if (data && typeof data === 'object' && 'error' in data && !('uuid' in data)) {
      throw new LogseqHttpError(String(data.error), undefined, data);
    }

    return data as T;
  }

  // ============== Page Operations ==============

  /**
   * Get a page by title or UUID
   */
  async getPage(titleOrUuid: string): Promise<Page | null> {
    return this.call<Page | null>("logseq.Editor.getPage", [titleOrUuid]);
  }

  /**
   * Get all pages in the graph
   */
  async getAllPages(): Promise<Page[]> {
    return this.call<Page[]>("logseq.Editor.getAllPages", []);
  }

  /**
   * Get blocks tree for a page
   */
  async getPageBlocksTree(pageTitle: string): Promise<Block[]> {
    return this.call<Block[]>("logseq.Editor.getPageBlocksTree", [pageTitle]);
  }

  /**
   * Create a new page
   */
  async createPage(
    title: string,
    properties?: Record<string, unknown>,
    options?: { createFirstBlock?: boolean; redirect?: boolean }
  ): Promise<Page | null> {
    return this.call<Page | null>("logseq.Editor.createPage", [
      title,
      properties ?? {},
      options ?? { createFirstBlock: true },
    ]);
  }

  /**
   * Delete a page
   */
  async deletePage(title: string): Promise<void> {
    await this.call<void>("logseq.Editor.deletePage", [title]);
  }

  // ============== Block Operations ==============

  /**
   * Get a block by UUID
   */
  async getBlock(uuid: string): Promise<Block | null> {
    return this.call<Block | null>("logseq.Editor.getBlock", [uuid]);
  }

  /**
   * Insert a new block
   */
  async insertBlock(
    parent: string,
    content: string,
    options?: { sibling?: boolean; before?: boolean; properties?: Record<string, unknown> }
  ): Promise<Block | null> {
    return this.call<Block | null>("logseq.Editor.insertBlock", [
      parent,
      content,
      options ?? {},
    ]);
  }

  /**
   * Update block content
   */
  async updateBlock(uuid: string, content: string): Promise<void> {
    await this.call<void>("logseq.Editor.updateBlock", [uuid, content]);
  }

  /**
   * Remove a block
   */
  async removeBlock(uuid: string): Promise<void> {
    await this.call<void>("logseq.Editor.removeBlock", [uuid]);
  }

  /**
   * Move a block
   */
  async moveBlock(
    uuid: string,
    targetUuid: string,
    options?: { before?: boolean; children?: boolean }
  ): Promise<void> {
    await this.call<void>("logseq.Editor.moveBlock", [
      uuid,
      targetUuid,
      options ?? {},
    ]);
  }

  // ============== Property Operations ==============

  /**
   * Get block properties
   */
  async getBlockProperties(uuid: string): Promise<Record<string, unknown>> {
    return this.call<Record<string, unknown>>("logseq.Editor.getBlockProperties", [uuid]);
  }

  /**
   * Upsert a block property
   */
  async upsertBlockProperty(
    uuid: string,
    key: string,
    value: unknown
  ): Promise<void> {
    await this.call<void>("logseq.Editor.upsertBlockProperty", [uuid, key, value]);
  }

  /**
   * Remove a block property
   */
  async removeBlockProperty(uuid: string, key: string): Promise<void> {
    await this.call<void>("logseq.Editor.removeBlockProperty", [uuid, key]);
  }

  // ============== Search & Query ==============

  /**
   * Search blocks by text
   */
  async search(query: string): Promise<SearchResult[]> {
    const results = await this.call<Array<{ block: Block }>>(
      "logseq.App.search",
      [query]
    );
    return results.map((r) => ({
      uuid: r.block.uuid,
      content: r.block.content,
      page: r.block.page?.name ?? "unknown",
    }));
  }

  /**
   * Execute a Datalog query
   */
  async datascriptQuery<T = unknown>(query: string): Promise<T[]> {
    return this.call<T[]>("logseq.DB.datascriptQuery", [query]);
  }

  /**
   * Execute a Datalog query with inputs
   */
  async q<T = unknown>(query: string, ...inputs: unknown[]): Promise<T[]> {
    return this.call<T[]>("logseq.DB.q", [query, ...inputs]);
  }

  // ============== Graph Info ==============

  /**
   * Get current graph info
   */
  async getCurrentGraph(): Promise<{ name: string; path: string } | null> {
    return this.call<{ name: string; path: string } | null>(
      "logseq.App.getCurrentGraph",
      []
    );
  }

  /**
   * Get user configuration
   */
  async getUserConfigs(): Promise<Record<string, unknown>> {
    return this.call<Record<string, unknown>>("logseq.App.getUserConfigs", []);
  }

  // ============== Utility ==============

  /**
   * Test the connection to Logseq
   */
  async testConnection(): Promise<boolean> {
    try {
      const graph = await this.getCurrentGraph();
      return graph !== null;
    } catch {
      return false;
    }
  }

  /**
   * Show a message in Logseq UI
   */
  async showMsg(
    message: string,
    status?: "success" | "warning" | "error"
  ): Promise<void> {
    await this.call<void>("logseq.App.showMsg", [message, status ?? "success"]);
  }
}

/**
 * Create a client from environment variables
 *
 * Supported environment variables:
 * - LOGSEQ_API_TOKEN (required): Authorization token from Logseq
 * - LOGSEQ_API_URL: Full URL (e.g., "http://192.168.1.100:45454")
 * - LOGSEQ_API_HOST: Host address (default: "127.0.0.1")
 * - LOGSEQ_API_PORT: Port number (default: "12315")
 *
 * Priority: LOGSEQ_API_URL takes precedence over HOST/PORT combination
 */
export function createClientFromEnv(): LogseqHttpClient {
  const token = process.env.LOGSEQ_API_TOKEN;

  if (!token) {
    throw new Error("LOGSEQ_API_TOKEN environment variable is required");
  }

  // Build URL from either full URL or host/port combination
  const url = getConfiguredUrl();

  return new LogseqHttpClient({ url, token });
}

/**
 * Get the configured API URL for display/debugging
 */
export function getConfiguredUrl(): string {
  if (process.env.LOGSEQ_API_URL) {
    return process.env.LOGSEQ_API_URL;
  }
  const host = process.env.LOGSEQ_API_HOST ?? "127.0.0.1";
  const port = process.env.LOGSEQ_API_PORT ?? "12315";
  return `http://${host}:${port}`;
}
