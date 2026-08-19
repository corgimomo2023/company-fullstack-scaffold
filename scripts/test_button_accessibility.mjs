import { readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const frontend = path.join(root, "frontend");
const requireFromFrontend = createRequire(path.join(frontend, "package.json"));
const { chromium } = requireFromFrontend("@playwright/test");
const React = requireFromFrontend("react");
const { renderToStaticMarkup } = requireFromFrontend("react-dom/server");
const { createServer } = requireFromFrontend("vite");
const vite = await createServer({
  root: frontend,
  appType: "custom",
  server: { middlewareMode: true },
});

let browser;
try {
  const { Button } = await vite.ssrLoadModule("/src/components/Button.tsx");
  const styles = await readFile(path.join(frontend, "src/styles.css"), "utf8");
  const markup = renderToStaticMarkup(
    React.createElement(
      Button,
      { pending: true, pendingLabel: "Creating project" },
      "Create project",
    ),
  );

  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(`<style>${styles}</style>${markup}`);
  const button = page.getByRole("button");
  const snapshot = await button.ariaSnapshot();
  const status = page.getByRole("status");
  const statusSnapshot = await status.ariaSnapshot();
  const statusBox = await status.boundingBox();
  const statusStyle = await status.evaluate((element) => {
    const computed = getComputedStyle(element);
    return { position: computed.position, overflow: computed.overflow };
  });
  const browserNameIsStable = snapshot.startsWith('- button "Create project"');
  const statusIsAnnounced = statusSnapshot.includes("Creating project");
  const statusIsVisuallyHidden =
    statusBox !== null &&
    statusBox.width <= 1 &&
    statusBox.height <= 1 &&
    statusStyle.position === "absolute" &&
    statusStyle.overflow === "hidden";

  if (!browserNameIsStable || !statusIsAnnounced || !statusIsVisuallyHidden) {
    console.error(
      JSON.stringify(
        {
          expectedName: "Create project",
          ariaSnapshot: snapshot,
          statusSnapshot,
          statusBox,
          statusStyle,
          markup,
        },
        null,
        2,
      ),
    );
    process.exitCode = 1;
  } else {
    console.log(
      JSON.stringify({
        accessibleName: "Create project",
        ariaSnapshot: snapshot,
        statusSnapshot,
        statusBox,
        pending: true,
      }),
    );
  }
} finally {
  await browser?.close();
  await vite.close();
}
