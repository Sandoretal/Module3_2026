// Builds .ics calendar files from the schedule tables on schedule.html,
// so the calendar always matches what the page shows.
(() => {
  const TZ = "Europe/London";
  const VTIMEZONE = [
    "BEGIN:VTIMEZONE",
    "TZID:Europe/London",
    "BEGIN:DAYLIGHT",
    "TZOFFSETFROM:+0000",
    "TZOFFSETTO:+0100",
    "TZNAME:BST",
    "DTSTART:19700329T010000",
    "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
    "END:DAYLIGHT",
    "BEGIN:STANDARD",
    "TZOFFSETFROM:+0100",
    "TZOFFSETTO:+0000",
    "TZNAME:GMT",
    "DTSTART:19701025T020000",
    "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
    "END:STANDARD",
    "END:VTIMEZONE"
  ];

  const escapeText = (value) =>
    value.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n");

  // Fold lines longer than 75 bytes (UTF-8), as the iCalendar format requires,
  // without splitting a multi-byte character.
  const encoder = new TextEncoder();
  const fold = (line) => {
    const parts = [];
    let current = "";
    for (const char of line) {
      if (encoder.encode(current + char).length > 75) {
        parts.push(current);
        current = " ";
      }
      current += char;
    }
    parts.push(current);
    return parts.join("\r\n");
  };

  const cellText = (cell) => (cell ? cell.textContent.replace(/\s+/g, " ").trim() : "");

  function eventsForDay(section) {
    const date = section.dataset.date.replace(/-/g, "");
    const events = [];
    section.querySelectorAll("tbody tr").forEach((row, index) => {
      if (row.classList.contains("study-row")) {
        return;
      }
      const [timeCell, sessionCell, typeCell, roomCell, leadCell] = row.querySelectorAll("td");
      const match = cellText(timeCell).match(/(\d{1,2}):(\d{2})\D+(\d{1,2}):(\d{2})/);
      if (!match) {
        return;
      }
      const [, h1, m1, h2, m2] = match;
      const pad = (n) => String(n).padStart(2, "0");

      // Session title is the text before the first <br>; any link becomes the event URL.
      const firstLine = sessionCell.innerHTML.split(/<br\s*\/?>/i)[0];
      const scratch = document.createElement("div");
      scratch.innerHTML = firstLine;
      let title = cellText(scratch);
      const link = sessionCell.querySelector("a");
      const tutorial = link && link.textContent.match(/Tutorial \d/);
      if (tutorial) {
        title = `${tutorial[0]}: ${title}`;
      }

      const details = [`Type: ${cellText(typeCell)}`, `Led by: ${cellText(leadCell)}`];
      if (link) {
        details.push(`${cellText(link)}: ${link.href}`);
      }
      details.push(`Timetable: ${location.href.split("#")[0]}`);

      events.push([
        "BEGIN:VEVENT",
        `UID:module3-${section.dataset.date}-${index}@sandoretal.github.io`,
        `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+/, "")}`,
        `DTSTART;TZID=${TZ}:${date}T${pad(h1)}${m1}00`,
        `DTEND;TZID=${TZ}:${date}T${pad(h2)}${m2}00`,
        `SUMMARY:${escapeText(`Module 3 – ${title}`)}`,
        `LOCATION:${escapeText(cellText(roomCell))}`,
        `DESCRIPTION:${escapeText(details.join("\n"))}`,
        ...(link ? [`URL:${link.href}`] : []),
        "END:VEVENT"
      ]);
    });
    return events;
  }

  function download(sections, filename) {
    const lines = [
      "BEGIN:VCALENDAR",
      "VERSION:2.0",
      "PRODID:-//Module 3 2026//Schedule//EN",
      "CALSCALE:GREGORIAN",
      "METHOD:PUBLISH",
      "X-WR-CALNAME:Module 3 timetable",
      `X-WR-TIMEZONE:${TZ}`,
      ...VTIMEZONE,
      ...sections.flatMap(eventsForDay).flat(),
      "END:VCALENDAR"
    ];
    const blob = new Blob([lines.map(fold).join("\r\n") + "\r\n"], { type: "text/calendar;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-calendar]");
    if (!button) {
      return;
    }
    const all = [...document.querySelectorAll(".schedule-day")];
    if (button.dataset.calendar === "all") {
      download(all, "module3-timetable.ics");
    } else {
      const section = button.closest(".schedule-day");
      download([section], `module3-${section.dataset.date}.ics`);
    }
  });
})();
