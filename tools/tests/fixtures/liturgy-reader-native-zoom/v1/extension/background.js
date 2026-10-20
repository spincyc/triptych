'use strict';
chrome.runtime.onInstalled.addListener(function () {
  chrome.tabs.create({ url: chrome.runtime.getURL('control.html'), active: false });
});
