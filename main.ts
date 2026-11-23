// post-x-the-agent-builds-a-game entry: hand the house the X post's address.
// The grader runs this with MAKEFUN_OUTPUT_DIR set; POST.json sits beside it.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const postFile = join(here, "POST.json");

// Fail loudly rather than hand the house a malformed address: the gate reads
// POST.json first, and a bad shape scores the entry 0.
const post = JSON.parse(readFileSync(postFile, "utf8"));
const urlPattern = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+\/?([?#].*)?$/;
if (typeof post.url !== "string" || !urlPattern.test(post.url)) {
  throw new Error("POST.json url is not an X post address: " + String(post.url));
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(postFile, join(outDir, "POST.json"));
console.log("POST.json ->", join(outDir, "POST.json"), "| url:", post.url);
