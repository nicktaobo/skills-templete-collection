// Paste this into browser console at each target viewport.
(() => {
  const root = document.documentElement;
  const overflow = root.scrollWidth > root.clientWidth;
  const offenders = [...document.querySelectorAll("*")]
    .filter((el) => el.scrollWidth > root.clientWidth)
    .slice(0, 30)
    .map((el) => ({
      tag: el.tagName,
      id: el.id || undefined,
      className: String(el.className || "").slice(0, 160),
      width: el.scrollWidth,
      viewport: root.clientWidth,
      text: el.textContent?.replace(/\s+/g, " ").trim().slice(0, 100),
    }));

  console.table(offenders);
  return {
    overflow,
    viewport: root.clientWidth,
    scrollWidth: root.scrollWidth,
    offenders,
  };
})();
