// Lists every PDF in the repo's slides/ folder, on slides.html and in the "Slides" card on
// resources.html. It asks the GitHub API for the folder's contents when the page loads, so a
// PDF added to slides/ on GitHub appears here without editing any HTML. If the request fails
// (offline, or GitHub's limit of 60 requests an hour per visitor is reached), the links
// already written in the HTML stay as they are.
//
// Any element with data-slides-list is filled: data-slides-list="cards" gives one card per
// PDF with Open and Download buttons; any other value gives a plain list of links.
(() => {
  const REPO = "Sandoretal/Module3_2026";
  const FOLDER = "slides";
  const CARD_COLOURS = ["cool", "hot", "pop"];
  const targets = document.querySelectorAll("[data-slides-list]");
  if (!targets.length) return;

  // "Module3_Module_Overview_part1.pdf" -> "Module3 Module Overview part1"
  const titleFrom = (name) => name.replace(/\.pdf$/i, "").replace(/[_-]+/g, " ").trim();

  const el = (tag, props = {}, children = []) => {
    const node = Object.assign(document.createElement(tag), props);
    node.append(...children);
    return node;
  };

  const asListItem = (pdf) =>
    el("li", {}, [el("a", { href: pdf.html_url, textContent: `${titleFrom(pdf.name)} (PDF)` })]);

  const asCard = (pdf, i) => {
    const download = el("a", { className: "button secondary small", href: pdf.download_url, textContent: "↓ Download" });
    download.setAttribute("download", "");
    return el("article", { className: `card ${CARD_COLOURS[i % CARD_COLOURS.length]}` }, [
      el("h3", { textContent: titleFrom(pdf.name) }),
      el("div", { className: "cta-row" }, [
        el("a", { className: "button primary small", href: pdf.html_url, textContent: "Open" }),
        download,
      ]),
    ]);
  };

  fetch(`https://api.github.com/repos/${REPO}/contents/${FOLDER}?ref=main`)
    .then((response) => {
      if (!response.ok) throw new Error(`GitHub API returned ${response.status}`);
      return response.json();
    })
    .then((items) => {
      const pdfs = items
        .filter((item) => item.type === "file" && /\.pdf$/i.test(item.name))
        .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));

      targets.forEach((target) => {
        const cards = target.dataset.slidesList === "cards";
        if (!pdfs.length) {
          target.replaceChildren(el(cards ? "p" : "li", { textContent: "No slides yet." }));
        } else {
          target.replaceChildren(...pdfs.map(cards ? asCard : asListItem));
        }
      });
    })
    .catch((error) => console.warn("Could not load the slides list:", error));
})();
