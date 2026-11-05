// Fills the "Slides" card on resources.html with every PDF in the repo's slides/ folder.
// It asks the GitHub API for the folder's contents when the page loads, so a PDF added
// to slides/ on GitHub appears here without editing any HTML. If the request fails
// (offline, or GitHub's limit of 60 requests an hour per visitor is reached), the links
// already written in the HTML stay as they are.
(() => {
  const REPO = "Sandoretal/Module3_2026";
  const FOLDER = "slides";
  const list = document.getElementById("slidesList");
  if (!list) return;

  // "Module3_Module_Overview_part1.pdf" -> "Module3 Module Overview part1"
  const titleFrom = (name) => name.replace(/\.pdf$/i, "").replace(/[_-]+/g, " ").trim();

  fetch(`https://api.github.com/repos/${REPO}/contents/${FOLDER}?ref=main`)
    .then((response) => {
      if (!response.ok) throw new Error(`GitHub API returned ${response.status}`);
      return response.json();
    })
    .then((items) => {
      const pdfs = items
        .filter((item) => item.type === "file" && /\.pdf$/i.test(item.name))
        .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true }));

      list.replaceChildren(
        ...(pdfs.length
          ? pdfs.map((pdf) => {
              const li = document.createElement("li");
              const a = document.createElement("a");
              a.href = pdf.html_url;
              a.textContent = `${titleFrom(pdf.name)} (PDF)`;
              li.append(a);
              return li;
            })
          : [Object.assign(document.createElement("li"), { textContent: "No slides yet." })])
      );
    })
    .catch((error) => console.warn("Could not load the slides list:", error));
})();
