// src/auth/tokenStore.ts — access token stored in MEMORY only, never localStorage (per instruction.md §7)
let _accessToken: string | null = null;

export const tokenStore = {
  get: (): string | null => _accessToken,
  set: (token: string): void => {
    _accessToken = token;
  },
  clear: (): void => {
    _accessToken = null;
  },
};
