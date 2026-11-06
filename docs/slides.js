// Lists every PDF in the repo's slides/ folder on the website. It asks the GitHub API for the
// folder's contents when a page loads, so a PDF added to slides/ on GitHub appears without
// editing any HTML. If the request fails (offline, or GitHub's limit of 60 requests an hour
// per visitor is reached), the links already written in the HTML stay as they are.
//
// Where the slides appear:
// - data-slides-list="cards"  (slides.html)     one card per PDF, with Open and Download buttons;
// - data-slides-list="by-day" (resources.html)  links grouped under each day of the schedule;
// - data-slides-list="list"                     a plain list of links;
// - data-slides="<lecture id>" (schedule.html)  a "Slides (PDF)" link under that lecture;
// - data-slides-rows (the "All indexed files" table on resources.html)  one row per PDF, of
//   type "slides", tagged with its lecture's tutorial so the Tutorial filter finds it.
//   A "slides:loaded" event is fired afterwards so the table's filters can re-apply.
//
// A PDF belongs to a lecture when its file name contains one of the lecture's words as whole
// words, ignoring case and treating spaces, "_" and "-" alike. For example, "time_series"
// matches "Lecture2_Time_Series.pdf", and "ml" matches "Intro_ML.pdf" but not "html".
// The part number also sets the day: "part2" (or "part 2", "Part_2") goes to Day 2, and so on.
// PDFs that match no lecture are listed under "Other slides".
(() => {
  const REPO = "Sandoretal/Module3_2026";
  const FOLDER = "slides";
  const CARD_COLOURS = ["cool", "hot", "pop"];

  // One entry per lecture on schedule.html, in schedule order. `tutorial` is the tutorial the
  // lecture introduces ("" for none), used by the file table's Tutorial filter. `day` must match the
  // section id on schedule.html ("day-2026-11-05") so the day headings can link to it.
  const DAYS = [
    { id: "day-2026-11-05", label: "Day 1 · Thursday 5 November" },
    { id: "day-2026-11-06", label: "Day 2 · Friday 6 November" },
    { id: "day-2026-11-09", label: "Day 3 · Monday 9 November" },
    { id: "day-2026-11-10", label: "Day 4 · Tuesday 10 November" },
  ];
  const LECTURES = [
    { id: "overview", tutorial: "", day: "day-2026-11-05", words: ["overview", "part1", "part_1"] },
    { id: "programming", tutorial: "1", day: "day-2026-11-05", words: ["programming", "python"] },
    { id: "time-series", tutorial: "2", day: "day-2026-11-06", words: ["time_series", "timeseries", "wearable", "wearables", "part2", "part_2"] },
    { id: "statistics", tutorial: "3", day: "day-2026-11-09", words: ["statistics", "ehr", "part3", "part_3"] },
    { id: "machine-learning", tutorial: "4", day: "day-2026-11-10", words: ["machine_learning", "ml", "part4", "part_4"] },
  ];

  const targets = document.querySelectorAll("[data-slides-list]");
  const lectureCells = document.querySelectorAll("[data-slides]");
  const fileTable = document.querySelector("[data-slides-rows]");
  if (!targets.length && !lectureCells.length && !fileTable) return;

  // "Module3_Module_Overview_part1.pdf" -> "_module3_module_overview_part1_"
  const words = (text) => `_${text.replace(/\.pdf$/i, "").toLowerCase().replace(/[^a-z0-9]+/g, "_")}_`;
  // "Module3_Module_Overview_part1.pdf" -> "Module3 Module Overview part1"
  const titleFrom = (name) => name.replace(/\.pdf$/i, "").replace(/[_-]+/g, " ").trim();
  const matchesLecture = (pdf, lecture) => lecture.words.some((w) => words(pdf.name).includes(words(w)));

  const el = (tag, props = {}, children = []) => {
    const node = Object.assign(document.createElement(tag), props);
    node.append(...children);
    return node;
  };

  const pdfLink = (pdf) => el("a", { href: pdf.html_url, textContent: `${titleFrom(pdf.name)} (PDF)` });
  const asListItem = (pdf) => el("li", {}, [pdfLink(pdf)]);

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

  // One <li> per day: the day (linking to it on the schedule), then that day's slides.
  const byDay = (pdfs) => {
    const unmatched = pdfs.filter((pdf) => !LECTURES.some((lecture) => matchesLecture(pdf, lecture)));
    const groups = DAYS.map((day) => ({
      label: day.label,
      href: `schedule.html#${day.id}`,
      pdfs: pdfs.filter((pdf) =>
        LECTURES.some((lecture) => lecture.day === day.id && matchesLecture(pdf, lecture))),
    }));
    if (unmatched.length) groups.push({ label: "Other slides", pdfs: unmatched });

    return groups.map((group) =>
      el("li", {}, [
        group.href
          ? el("a", { href: group.href, title: "See this day on the schedule" }, [el("strong", { textContent: group.label })])
          : el("strong", { textContent: group.label }),
        group.pdfs.length
          ? el("ul", {}, group.pdfs.map(asListItem))
          : el("ul", {}, [el("li", { className: "empty", textContent: "No slides yet" })]),
      ]));
  };

  // A row for the "All indexed files" table, in the same shape as the hand-written rows.
  const asTableRow = (pdf) => {
    const lecture = LECTURES.find((l) => matchesLecture(pdf, l));
    const day = lecture && DAYS.find((d) => d.id === lecture.day);
    const row = el("tr", {}, [
      el("td", { textContent: FOLDER }),
      el("td", { textContent: pdf.name }),
      el("td", { textContent: "slides" }),
      el("td", {}, [el("a", { href: pdf.html_url, textContent: "Open" })]),
    ]);
    row.dataset.type = "slides";
    row.dataset.tutorial = lecture ? lecture.tutorial : "";
    row.dataset.search = `slides lecture pdf ${titleFrom(pdf.name)} ${day ? day.label : ""}`.toLowerCase();
    return row;
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
        const style = target.dataset.slidesList;
        if (!pdfs.length) {
          target.replaceChildren(el(style === "cards" ? "p" : "li", { textContent: "No slides yet." }));
        } else if (style === "cards") {
          target.replaceChildren(...pdfs.map(asCard));
        } else if (style === "by-day") {
          target.replaceChildren(...byDay(pdfs));
        } else {
          target.replaceChildren(...pdfs.map(asListItem));
        }
      });

      lectureCells.forEach((cell) => {
        const lecture = LECTURES.find((l) => l.id === cell.dataset.slides);
        if (!lecture) return;
        const matches = pdfs.filter((pdf) => matchesLecture(pdf, lecture));
        matches.forEach((pdf) => {
          const label = matches.length > 1 ? `Slides: ${titleFrom(pdf.name)} (PDF)` : "Slides (PDF)";
          cell.append(el("br"), el("a", { href: pdf.html_url, textContent: label }));
        });
      });

      if (fileTable) {
        fileTable.querySelectorAll('tr[data-type="slides"]').forEach((row) => row.remove());
        const before = fileTable.querySelector("#noMatches");
        pdfs.map(asTableRow).forEach((row) => fileTable.insertBefore(row, before));
        document.dispatchEvent(new Event("slides:loaded"));
      }
    })
    .catch((error) => console.warn("Could not load the slides list:", error));
})();
