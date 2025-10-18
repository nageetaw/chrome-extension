let port;

chrome.runtime.onConnectExternal.addListener((p) => {
  port = p;
  console.log("Connected to client:", p.name);
  port.onMessage.addListener(async (msg) => {
    if (msg.action === "open_tab") {
      await chrome.tabs.create({ url: msg.url });
    } else if (msg.action === "search") {
      const queryUrl = `https://www.google.com/search?q=${encodeURIComponent(
        msg.query
      )}`;
      await chrome.tabs.create({ url: queryUrl });
    }
  });
});
