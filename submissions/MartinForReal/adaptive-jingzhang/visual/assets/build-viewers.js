#!/usr/bin/env node
"use strict";

// Regenerates the two content sections of the offline viewers from the bilingual record.
//
// The viewers were hand-authored in each language, and they drifted: the English one
// listed a different set of renewal actions than the Chinese one and gave all three key
// areas roles that no registry record supports. Both sections are now generated, so a
// wording only ever exists once and neither language can move without the other.
//
// Only the `areas` and `projects` sections are generated. The stylesheet, navigation,
// hero, and every other section stay exactly as authored — this script replaces two
// elements, it does not rebuild the page.
//
// Each key-area card now also carries the five plates of its area: the language-matched
// raster, an anchor a reviewer can link to, a caption written from the design record, the
// registered long description behind a native disclosure, and a direct link to the
// full-resolution PNG. A viewer only ever serves its own language's rasters and its own
// language's descriptions, so an English reader is never sent a Chinese drawing and never
// sent a Chinese description of one.
//
// Usage: node build-viewers.js [--check]

const fs = require("node:fs");
const path = require("node:path");
const contract = require("./key-area-contract.js");

const ASSETS = __dirname;
const PACKAGE_ROOT = path.resolve(ASSETS, "..", "..");
const SOURCE = path.join(ASSETS, "regeneration-source.json");
const PLATES = path.join(ASSETS, "area-plates.json");
const DESIGN = path.join(ASSETS, "key-area-design.json");

const TARGETS = [
  { language: "zh", file: path.join(PACKAGE_ROOT, "visual", "index.html") },
  { language: "en", file: path.join(PACKAGE_ROOT, "visual", "index.en.html") },
];

// The viewers sit one directory below the package root, so a registered raster path is
// reached from here by stepping back up. The registered path itself is never rewritten,
// only prefixed, so a reader searching for it in the page still finds it verbatim.
const RASTER_PREFIX = "../";

// Reused from the existing stylesheet so the generated block needs no new CSS.
const ACCENTS = ["accent-teal", "accent-coral", "accent-violet"];

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// How many times a literal appears. Used where "present" is not the question — an id that
// appears twice is a different fault from an id that appears once.
function occurrences(haystack, needle) {
  let count = 0;
  let at = haystack.indexOf(needle);
  while (at !== -1) {
    count += 1;
    at = haystack.indexOf(needle, at + needle.length);
  }
  return count;
}

// Picks the value for one language out of a record that stores both as `<field>_zh` and
// `<field>_en`. A missing key is an authoring error, not something to paper over with an
// empty string, because an empty label would silently ship a blank cell.
function pick(record, field, language) {
  const key = `${field}_${language}`;
  if (!(key in record) || record[key] === null || record[key] === undefined) {
    throw new Error(`record is missing ${key}`);
  }
  return record[key];
}

// Locates a top-level <section> by its id and returns its bounds. Sections are not nested
// in these viewers; if that ever changes the naive end-tag scan would cut in the wrong
// place, so the assumption is checked rather than trusted.
function findSection(html, id) {
  const open = new RegExp(`<section[^>]*\\bid="${id}"[^>]*>`);
  const match = open.exec(html);
  if (!match) throw new Error(`no <section id="${id}"> found`);
  const start = match.index;
  const bodyStart = start + match[0].length;
  const end = html.indexOf("</section>", bodyStart);
  if (end === -1) throw new Error(`<section id="${id}"> is never closed`);
  if (html.slice(bodyStart, end).includes("<section")) {
    throw new Error(`<section id="${id}"> contains a nested section; the replacement bounds are unsafe`);
  }
  return { start, end: end + "</section>".length };
}

function replaceSection(html, id, replacement) {
  const bounds = findSection(html, id);
  return html.slice(0, bounds.start) + replacement + html.slice(bounds.end);
}

function table(headers, rows) {
  const head = headers.map((cell) => `<th>${escapeHtml(cell)}</th>`).join("");
  const body = rows
    .map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join("")}</tr>`)
    .join("");
  return `<table class="table"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;
}

// The anchor a reviewer, a board and the plate registry all use to point at the same
// drawing. Derived from the contract rather than written out thirty times.
function plateAnchor(area, concept, language) {
  return `plate-${area.prefix.toLowerCase()}-${concept.concept_id}-${language}`;
}

// The caption states what the drawing may be read as claiming. Everything in it comes from
// key-area-design.json; the Dazhongsi caption quotes the registered disclosure exactly.
function plateCaption(concept, design, language) {
  const zh = language === "zh";
  if (concept.concept_id === "01") {
    const parts = [pick(design.plan, "condition", language)];
    if (design.disclosure_zh || design.disclosure_en) parts.push(pick(design, "disclosure", language));
    return parts.join(zh ? "" : " ");
  }
  if (concept.concept_id === "02") {
    const elements = design.plan.elements.length;
    const cuts = design.plan.cut_keys.map((cut) => `${cut.key}→${cut.section_id}`).join(" ");
    return zh
      ? `${design.plan.id}：${elements} 个构成元素，剖切号 ${cuts}。`
      : `${design.plan.id}: ${elements} elements, cuts keyed ${cuts}.`;
  }
  if (concept.concept_id === "03") {
    const dimensions = design.sections.flatMap((section) => section.dimensions);
    const counted = (basis) => dimensions.filter((entry) => entry.basis_type === basis).length;
    return zh
      ? `${design.sections.map((section) => section.id).join(" / ")}：共 ${dimensions.length} 项尺寸，`
        + `${counted("proposed_module")} 项 proposed_module（以米计、未经核验）、`
        + `${counted("pending")} 项 pending（以米计、取值留空、附复算触发条件）。`
      : `${design.sections.map((section) => section.id).join(" / ")}: ${dimensions.length} dimensions — `
        + `${counted("proposed_module")} proposed_module, in metres and unverified, and `
        + `${counted("pending")} pending, left null in metres with a recalculation trigger.`;
  }
  if (concept.concept_id === "04") {
    const chain = design.step_free_chain;
    const seasonal = design.seasonal_operations;
    return zh
      ? `${chain.id}：${chain.nodes.length} 个节点 / ${chain.segments.length} 段，`
        + `${Object.keys(chain.equivalents).length} 类等效渠道，${chain.operating_modes.length} 种运行工况；`
        + `无障碍闸口 ${chain.status.accessibility_gate}；试点 ${seasonal.pilot.days} 天，`
        + `sufficient_for_year_round 为 false。`
      : `${chain.id}: ${chain.nodes.length} nodes across ${chain.segments.length} segments, `
        + `${Object.keys(chain.equivalents).length} equivalent channels, ${chain.operating_modes.length} operating modes; `
        + `accessibility gate ${chain.status.accessibility_gate}; a ${seasonal.pilot.days}-day pilot with `
        + `sufficient_for_year_round false.`;
  }
  const envelope = design.phase1_envelope;
  const thresholds = design.seasonal_operations.thresholds;
  return zh
    ? `${envelope.id}：not_authorized、unfunded，受 ${envelope.blocked_by.join(" ")} 阻断；`
      + `${thresholds.length} 项季节阈值（${thresholds.map((entry) => entry.id).join(" ")}）的 approved_threshold 均为空、`
      + `pilot_start_allowed 均为 false。`
    : `${envelope.id}: not_authorized, unfunded, blocked by ${envelope.blocked_by.join(" ")}; its `
      + `${thresholds.length} seasonal thresholds (${thresholds.map((entry) => entry.id).join(" ")}) all hold `
      + `approved_threshold null and pilot_start_allowed false.`;
}

// The id of the node that describes one plate at length. Derived the same way the anchor is,
// so the `aria-describedby` on the image and the `id` on the paragraph cannot drift apart and
// no two plates can ever claim the same description.
function plateDescriptionId(area, concept, language) {
  return `${plateAnchor(area, concept, language)}-description`;
}

// The five plates of one area, in contract order.
//
// Everything a reader who cannot see the drawing is given comes from the plate registry: the
// title, the short alt text, and the long description. The registry is written by the plate
// builder, which runs before this one, so a missing record means the two builders disagree
// about what exists and the build stops rather than inventing a substitute — a synthesised
// alt text would describe what this script assumes the drawing shows, not what it shows.
//
// The long description is too long to sit in an `alt` attribute and too important to drop, so
// it goes in a `<details>` a sighted reader can open and `aria-describedby` points the image
// at it. `<details>` is used rather than a scripted disclosure because it is keyboard
// operable and announced as a disclosure without any JavaScript, and these viewers must work
// from a file:// URL with nothing loaded from a network.
//
// The PNG is also linked directly. A plate is 1800 × 1200 and the card shows it at card
// width; a reviewer who needs to read a dimension string on the drawing needs the file, not a
// scaled copy of it.
function plateFigures(contractArea, design, language, labels, records) {
  return contract.CONCEPTS.map((concept) => {
    const plateId = contract.plateId(contractArea, concept);
    const artifactId = contract.artifactId(contractArea, concept, language);
    const record = records.get(artifactId);
    if (!record) throw new Error(`the plate registry has no record for ${artifactId}`);
    for (const field of ["title", "alt_text", "extended_description", "width_px", "height_px"]) {
      if (record[field] === null || record[field] === undefined || record[field] === "") {
        throw new Error(`${artifactId} has no ${field} in the plate registry`);
      }
    }
    if (record.language !== language) {
      throw new Error(`${artifactId} is registered as ${record.language}, not ${language}`);
    }
    const source = contract.plateFile(contractArea, concept, language);
    if (record.file !== source) {
      throw new Error(`${artifactId} is registered at ${record.file}, expected ${source}`);
    }
    const href = `${RASTER_PREFIX}${source}`;
    const descriptionId = plateDescriptionId(contractArea, concept, language);
    const linkLabel = `${pick(labels, "plate_full_resolution", language)} · ${plateId} · `
      + `${record.width_px} × ${record.height_px} px`;
    // The caption is flow content, so the description and the link live inside it: a
    // `<figcaption>` has to be the first or last child of its `<figure>`, and putting them
    // after it as siblings would make the caption neither.
    return `<figure class="figure" id="${plateAnchor(contractArea, concept, language)}">`
      + `<img src="${escapeHtml(href)}" width="${record.width_px}" height="${record.height_px}"`
      + ` alt="${escapeHtml(record.alt_text)}" aria-describedby="${descriptionId}">`
      + `<figcaption class="caption">`
      + `<p class="plate-title"><strong>${escapeHtml(record.title)}</strong> — ${escapeHtml(plateCaption(concept, design, language))}</p>`
      + `<details class="plate-note">`
      + `<summary>${escapeHtml(pick(labels, "drawing_plate_description", language))}</summary>`
      + `<p id="${descriptionId}">${escapeHtml(record.extended_description)}</p>`
      + `</details>`
      + `<p class="plate-link"><a href="${escapeHtml(href)}">${escapeHtml(linkLabel)}</a></p>`
      + `</figcaption></figure>`;
  }).join("");
}

function areaCard(area, labels, language, context, index) {
  const accent = ACCENTS[index % ACCENTS.length];
  const parts = [];
  parts.push(`<h3>${escapeHtml(pick(area, "name", language))}</h3>`);

  // The role is the wording the two viewers previously disagreed about, so it is printed
  // verbatim from the registry rather than paraphrased into a card subtitle.
  const role = pick(area, "role", language);
  const meta = [
    `${pick(labels, "role_label", language)}: ${role}`,
    `${pick(labels, "official_area", language)}: ${area.official_area_ha} ha`,
    area.lab,
  ];
  if (area.georeferenced === false) meta.push(pick(labels, "non_georeferenced", language));
  parts.push(`<p class="status">${escapeHtml(meta.join(" · "))}</p>`);
  parts.push(`<p>${escapeHtml(pick(area, "distinct_task", language))}</p>`);

  // An area whose position is disputed states that on its own card, next to its content,
  // rather than in a footnote a reader may never reach.
  if (area.georeferenced === false) {
    parts.push(`<div class="gate"><strong>${escapeHtml(pick(labels, "non_georeferenced", language))}</strong>`
      + `<p>${escapeHtml(pick(area, "non_station_note", language))}</p></div>`);
  }

  parts.push(`<h4>${escapeHtml(pick(labels, "components_heading", language))}</h4>`);
  parts.push(table(
    [
      pick(labels, "col_id", language),
      pick(labels, "col_name", language),
      pick(labels, "col_description", language),
      pick(labels, "col_evidence", language),
      pick(labels, "col_blocked", language),
    ],
    area.components.map((component) => [
      component.id,
      pick(component, "name", language),
      pick(component, "description", language),
      component.evidence_ref,
      component.blocked_by,
    ]),
  ));

  parts.push(`<h4>${escapeHtml(pick(labels, "routes_heading", language))}</h4>`);
  parts.push(table(
    [
      pick(labels, "col_id", language),
      pick(labels, "col_name", language),
      pick(labels, "col_description", language),
      pick(labels, "col_evidence", language),
      pick(labels, "col_blocked", language),
    ],
    area.routes.map((route) => {
      if (route.step_free !== true) {
        throw new Error(`${route.id} is published as a step-free chain but is not marked step_free`);
      }
      return [
        route.id,
        `${pick(route, "name", language)} (${pick(labels, "step_free", language)})`,
        pick(route, "description", language),
        route.evidence_ref,
        route.blocked_by,
      ];
    }),
  ));

  parts.push(`<p><strong>${escapeHtml(pick(labels, "winter", language))}:</strong> `
    + `${escapeHtml(pick(area, "winter", language))}</p>`);
  parts.push(`<p><strong>${escapeHtml(pick(labels, "maintenance", language))}:</strong> `
    + `${escapeHtml(pick(area, "maintenance", language))}</p>`);

  const envelope = area.phase1_envelope;
  const states = [
    envelope.id,
    envelope.reversible ? pick(labels, "reversible", language) : null,
    envelope.authorization_state === "not_authorized"
      ? pick(labels, "not_authorized", language)
      : envelope.authorization_state,
    envelope.funding_state === "unfunded" ? pick(labels, "unfunded", language) : envelope.funding_state,
    `${pick(labels, "col_blocked", language)}: ${envelope.blocked_by}`,
  ].filter(Boolean);
  parts.push(`<p><strong>${escapeHtml(pick(labels, "envelope", language))}:</strong> `
    + `${escapeHtml(pick(envelope, "description", language))}</p>`);
  parts.push(states.map((state) => `<span class="pill">${escapeHtml(state)}</span>`).join(""));

  const sheet = context.designAreas.get(area.id);
  const contractArea = contract.AREAS.find((entry) => entry.area_feature_id === area.id);
  // The register and the spatial record are joined on the feature id, so an area present in
  // one and missing from the other stops the build instead of shipping a card with no plates.
  if (!sheet) throw new Error(`${DESIGN} declares nothing for ${area.id}`);
  if (!contractArea) throw new Error(`${area.id} has no entry in the key-area contract`);
  parts.push(`<h4>${escapeHtml(pick(labels, "plates", language))}</h4>`);
  parts.push(plateFigures(contractArea, sheet, language, labels, context.records));

  return `<article class="card ${accent}">${parts.join("")}</article>`;
}

function areasSection(source, language, context) {
  const labels = source.ui_labels;
  const block = labels.areas;
  const cards = source.areas
    .map((area, index) => areaCard(area, labels, language, context, index))
    .join("");
  // The overview figure is carried through from the hand-authored section so regenerating
  // does not leave the rendered key-area image referenced by nothing.
  const figure = `<figure class="figure">`
    + `<img src="${escapeHtml(pick(block, "figure_src", language))}" alt="${escapeHtml(pick(block, "figure_alt", language))}">`
    + `<figcaption class="caption">${escapeHtml(pick(block, "figure_caption", language))}</figcaption>`
    + `</figure>`;
  return `<section class="section" id="areas">`
    + `<span class="eyebrow">${escapeHtml(pick(block, "eyebrow", language))}</span>`
    + `<h2>${escapeHtml(pick(block, "heading", language))}</h2>`
    + `<p class="intro">${escapeHtml(pick(block, "intro", language))}</p>`
    + figure
    + cards
    + `</section>`;
}

function projectsSection(source, language) {
  const labels = source.ui_labels;
  const block = labels.projects;
  const pills = source.projects
    .map((project) => `<span class="pill">${escapeHtml(`${project.id} ${pick(project, "name", language)}`)}</span>`)
    .join("");
  const rows = source.projects.map((project) => [project.id, pick(project, "name", language), project.phase]);
  return `<section class="section" id="projects">`
    + `<span class="eyebrow">${escapeHtml(pick(block, "eyebrow", language))}</span>`
    + `<h2>${escapeHtml(pick(block, "heading", language))}</h2>`
    + `<div>${pills}</div>`
    + `<p class="intro">${escapeHtml(pick(block, "intro", language))}</p>`
    + table(
      [pick(labels, "col_id", language), pick(labels, "col_name", language), pick(labels, "col_phase", language)],
      rows,
    )
    + `</section>`;
}

// Rewrites the opening paragraph of the hero from the bilingual record. The two viewers
// had put the same idea in different places — the Chinese one inside the lede, the English
// one in a bare paragraph after it — and the English one still named the generator after
// the lineage instead of the computation. Both are now one paragraph written from one
// record, and a hand-authored method paragraph directly after the lede is absorbed into it.
// The match stops at the first `</p>`, so the surrounding hero markup is untouched.
function stampHero(html, hero, language) {
  const lede = `<p class="lede">${escapeHtml(hero[`motto_${language}`])}<br>${escapeHtml(hero[`method_${language}`])}</p>`;
  const pattern = /<p class="lede">.*?<\/p>(\s*<p>(?!<a )[^]*?<\/p>)?/;
  const found = html.match(pattern);
  if (!found) throw new Error(`the ${language} viewer has no <p class="lede"> to stamp`);
  if (found[0] === lede) return { html, changed: false };
  return { html: html.replace(pattern, lede), changed: true };
}

function main(argv) {
  const checkOnly = argv.includes("--check");
  const source = readJson(SOURCE);
  const design = readJson(DESIGN);
  // The plate registry is produced by the plate builder, which runs before this one. It is
  // the only place the published title, alt text and long description of a drawing exist, so
  // it is required rather than optional: without it this script would have to describe
  // drawings it has never read. The raster paths and anchors still come from the contract and
  // must not move when a registry is regenerated.
  if (!fs.existsSync(PLATES)) throw new Error(`${PLATES} does not exist; run build-plates.js first`);
  const registry = readJson(PLATES);
  const context = {
    designAreas: new Map(design.areas.map((area) => [area.area_feature_id, area])),
    records: new Map((registry.artifacts ?? []).map((record) => [record.artifact_id, record])),
  };
  const artifacts = contract.expectedArtifacts();

  const failures = [];
  const results = [];
  let changedFiles = 0;

  for (const target of TARGETS) {
    const original = fs.readFileSync(target.file, "utf8");
    const hero = stampHero(original, source.viewer_hero, target.language);
    let output = replaceSection(hero.html, "areas", areasSection(source, target.language, context));
    output = replaceSection(output, "projects", projectsSection(source, target.language));
    const changed = output !== original;
    if (changed) changedFiles += 1;
    if (changed && !checkOnly) fs.writeFileSync(target.file, output, "utf8");

    const relative = path.relative(PACKAGE_ROOT, target.file).split(path.sep).join("/");
    for (const project of source.projects) {
      if (!output.includes(project.id)) failures.push(`${relative} does not list action ${project.id}`);
      if (!output.includes(project[`name_${target.language}`])) {
        failures.push(`${relative} does not use the registry title for ${project.id}`);
      }
    }
    for (const area of source.areas) {
      if (!output.includes(area[`role_${target.language}`])) {
        failures.push(`${relative} does not use the registry role for ${area.id}`);
      }
    }
    // A viewer carrying the other language's wording would mean the sections were
    // generated from the wrong column of the record.
    const other = target.language === "zh" ? "en" : "zh";
    for (const area of source.areas) {
      if (output.includes(area[`distinct_task_${other}`])) {
        failures.push(`${relative} carries the ${other} task text for ${area.id}`);
      }
    }
    if (!output.includes(escapeHtml(source.viewer_hero[`method_${target.language}`]))) {
      failures.push(`${relative} does not carry the hero method sentence from the bilingual record`);
    }
    // Every plate of this language must be reachable and shown here, and no raster of the
    // other language may appear: the Chinese path is not a substring of the English one, so
    // plain containment is exact in both directions.
    //
    // The non-visual half of a plate is checked the same way. An `aria-describedby` that
    // points at nothing, or at a node that also describes another drawing, is worse than no
    // description at all, because a screen reader announces it as if it belonged here — so
    // the description id is counted, not merely looked for.
    for (const artifact of artifacts) {
      const anchor = plateAnchor(artifact.area, artifact.concept, artifact.language);
      const descriptionId = plateDescriptionId(artifact.area, artifact.concept, artifact.language);
      const record = context.records.get(artifact.artifact_id);
      if (artifact.language === target.language) {
        if (!output.includes(`id="${anchor}"`)) failures.push(`${relative} has no anchor ${anchor}`);
        if (!output.includes(artifact.file)) failures.push(`${relative} never references ${artifact.file}`);
        const described = occurrences(output, `id="${descriptionId}"`);
        if (described !== 1) {
          failures.push(`${relative} carries ${described} nodes with id ${descriptionId}, expected exactly one`);
        }
        if (!output.includes(`aria-describedby="${descriptionId}"`)) {
          failures.push(`${relative} does not point ${artifact.artifact_id} at its long description`);
        }
        if (!output.includes(`href="${RASTER_PREFIX}${artifact.file}"`)) {
          failures.push(`${relative} offers no full-resolution link to ${artifact.file}`);
        }
        if (record && !output.includes(escapeHtml(record.extended_description))) {
          failures.push(`${relative} does not carry the registered long description of ${artifact.artifact_id}`);
        }
        if (record && !output.includes(`alt="${escapeHtml(record.alt_text)}"`)) {
          failures.push(`${relative} does not carry the registered alt text of ${artifact.artifact_id}`);
        }
      } else {
        if (output.includes(`id="${anchor}"`)) failures.push(`${relative} carries the ${artifact.language} anchor ${anchor}`);
        if (output.includes(artifact.file)) {
          failures.push(`${relative} references the ${artifact.language} raster ${artifact.file}`);
        }
        if (output.includes(descriptionId)) {
          failures.push(`${relative} carries the ${artifact.language} description id ${descriptionId}`);
        }
        if (record && output.includes(escapeHtml(record.extended_description))) {
          failures.push(`${relative} carries the ${artifact.language} long description of ${artifact.artifact_id}`);
        }
      }
    }
    // The Dazhongsi limit is quoted rather than paraphrased, and only in this page's own
    // language: a reader of the English viewer is not asked to read a Chinese footnote.
    const otherLanguage = target.language === "zh" ? "en" : "zh";
    const disclosures = { zh: contract.DZS_DISCLOSURE_ZH, en: contract.DZS_DISCLOSURE_EN };
    if (!output.includes(escapeHtml(disclosures[target.language]))) {
      failures.push(`${relative} does not carry the Issue #1029 disclosure in ${target.language}`);
    }
    if (output.includes(escapeHtml(disclosures[otherLanguage]))) {
      failures.push(`${relative} carries the ${otherLanguage} Issue #1029 disclosure`);
    }
    results.push({ file: relative, language: target.language, changed, hero_stamped: hero.changed });
  }

  const report = {
    status: failures.length === 0 ? "PASS" : "FAIL",
    exit_code: failures.length === 0 ? (checkOnly && changedFiles > 0 ? 1 : 0) : 1,
    mode: checkOnly ? "check" : "write",
    changed_files: changedFiles,
    areas: source.areas.length,
    projects: source.projects.length,
    plates_shown: artifacts.length / contract.LANGUAGES.length,
    registry_titles_available: context.records.size,
    failures,
    results,
  };
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  return report.exit_code;
}

if (require.main === module) {
  try {
    process.exitCode = main(process.argv.slice(2));
  } catch (error) {
    process.stdout.write(`${JSON.stringify({
      status: "FAIL",
      exit_code: 2,
      error_type: "build_error",
      error: error instanceof Error ? error.message : String(error),
    }, null, 2)}\n`);
    process.exitCode = 2;
  }
}

module.exports = {
  findSection,
  replaceSection,
  areasSection,
  projectsSection,
  plateAnchor,
  plateDescriptionId,
  plateFigures,
};
