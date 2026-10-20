'use strict';
const events = [];
chrome.tabs.onZoomChange.addListener(function (event) { events.push(event); });
async function describe(tabId) {
  const tab = await chrome.tabs.get(tabId);
  const window = await chrome.windows.get(tab.windowId);
  return {
    reportedZoomFactor: await chrome.tabs.getZoom(tabId),
    settings: await chrome.tabs.getZoomSettings(tabId),
    tab: { id: tab.id, windowId: tab.windowId, width: tab.width, height: tab.height,
      url: tab.url, status: tab.status },
    window: { id: window.id, left: window.left, top: window.top,
      width: window.width, height: window.height, state: window.state },
    events: events.filter(function (event) { return event.tabId === tabId; })
  };
}
window.ReaderNativeZoom = Object.freeze({
  async create(url) {
    if (!/^http:\/\/127\.0\.0\.1:\d+\//.test(url)) throw new Error('local artifact only');
    const tab = await chrome.tabs.create({ url: url, active: true });
    return { tabId: tab.id, windowId: tab.windowId };
  },
  async set(tabId, factor) {
    if (factor !== 1 && factor !== 4) throw new Error('only 100% and 400% are in this probe');
    // Automatic mode makes the browser perform the scaling. Manual mode would
    // ask extension code to scale the page and would not establish this claim.
    await chrome.tabs.setZoomSettings(tabId, { mode: 'automatic', scope: 'per-tab' });
    await chrome.tabs.setZoom(tabId, factor);
    return describe(tabId);
  },
  describe: describe,
  async remove(tabId) { await chrome.tabs.remove(tabId); }
});
