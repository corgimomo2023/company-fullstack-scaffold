const pptxgen = require('pptxgenjs');
const path = require('path');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Internal AI Model Evaluation Team';
pptx.company = 'Asia Allied Corporate Digital';
pptx.subject = 'Version 4 research-backed AI vibe-coding model evaluation';
pptx.title = 'AI Vibe Coding Model Comparison — V4 Deck';
pptx.lang = 'en-HK';
pptx.theme = {
  headFontFace: 'Arial',
  bodyFontFace: 'Arial',
  lang: 'en-HK'
};
pptx.defineSlideMaster({
  title: 'LIGHT',
  background: { color: 'F7F7F7' },
  objects: [
    { text: { text: 'AI VIBE CODING · MODEL EVALUATION V4', options: { x: 0.6, y: 0.2, w: 5.6, h: 0.2, fontFace: 'Arial', fontSize: 9, bold: true, color: '6C757D', margin: 0 } } },
    { text: { text: '2026-08-17', options: { x: 11.7, y: 0.2, w: 1.0, h: 0.2, fontFace: 'Arial', fontSize: 9, color: '6C757D', align: 'right', margin: 0 } } },
  ],
  slideNumber: { x: 12.4, y: 7.08, w: 0.3, h: 0.18, fontFace: 'Arial', fontSize: 9, color: '6C757D', align: 'right', margin: 0 }
});
pptx.defineSlideMaster({
  title: 'DARK',
  background: { color: '003531' },
  objects: [
    { text: { text: 'AI VIBE CODING · MODEL EVALUATION V4', options: { x: 0.6, y: 0.2, w: 5.6, h: 0.2, fontFace: 'Arial', fontSize: 9, bold: true, color: 'B7DCD8', margin: 0 } } },
    { text: { text: '2026-08-17', options: { x: 11.7, y: 0.2, w: 1.0, h: 0.2, fontFace: 'Arial', fontSize: 9, color: 'B7DCD8', align: 'right', margin: 0 } } },
  ],
  slideNumber: { x: 12.4, y: 7.08, w: 0.3, h: 0.18, fontFace: 'Arial', fontSize: 9, color: 'B7DCD8', align: 'right', margin: 0 }
});

const C = {
  green: '006A63',
  dark: '003531',
  active: '001C19',
  orange: 'E6762D',
  orangeDark: 'B15315',
  orangePale: 'FFF2EA',
  text: '333333',
  muted: '6C757D',
  white: 'FFFFFF',
  bg: 'F7F7F7',
  border: 'CECECE',
  soft: 'E7F3F1',
  soft2: 'D7EAE8',
  gray: 'ECECEC',
  danger: 'DC3545'
};

const HERO_IMAGE = path.join(__dirname, '..', '..', 'docs', 'reports', 'assets', 'v4-deck-ai-evaluation-hero.jpg');

function addTitle(slide, eyebrow, title, subtitle, dark = false) {
  slide.addText(eyebrow.toUpperCase(), { x: 0.65, y: 0.62, w: 4.6, h: 0.28, fontFace: 'Arial', fontSize: 11, bold: true, color: dark ? 'E9A36F' : C.orangeDark, charSpacing: 1.5, margin: 0 });
  slide.addText(title, { x: 0.65, y: 1.02, w: 11.9, h: 0.68, fontFace: 'Arial', fontSize: 34, bold: true, color: dark ? C.white : C.dark, margin: 0, breakLine: false, fit: 'shrink' });
  if (subtitle) slide.addText(subtitle, { x: 0.65, y: 1.82, w: 11.4, h: 0.48, fontFace: 'Arial', fontSize: 15, color: dark ? 'D7EAE8' : C.muted, margin: 0, fit: 'shrink' });
}
function addSource(slide, text, dark = false) {
  slide.addText(text, { x: 0.65, y: 7.05, w: 11.4, h: 0.18, fontFace: 'Arial', fontSize: 8, color: dark ? 'B7DCD8' : '6C757D', margin: 0, fit: 'shrink' });
}
function card(slide, x, y, w, h, opts = {}) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.08,
    fill: { color: opts.fill || C.white, transparency: opts.transparency || 0 },
    line: { color: opts.line || (opts.fill || C.white), transparency: opts.lineTransparency ?? 100 },
    shadow: opts.shadow === false ? undefined : { type: 'outer', color: '003531', opacity: 0.10, blur: 1.5, angle: 45, distance: 1 }
  });
}
function pill(slide, text, x, y, w, fill = C.soft, color = C.green) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.32, rectRadius: 0.16, fill: { color: fill }, line: { color: fill, transparency: 100 } });
  slide.addText(text, { x, y: y + 0.03, w, h: 0.22, fontFace: 'Arial', fontSize: 10, bold: true, color, align: 'center', margin: 0, fit: 'shrink' });
}
function bullet(slide, text, x, y, w, color = C.text, size = 15) {
  slide.addShape(pptx.ShapeType.ellipse, { x, y: y + 0.08, w: 0.12, h: 0.12, fill: { color: C.orange }, line: { color: C.orange, transparency: 100 } });
  slide.addText(text, { x: x + 0.24, y, w: w - 0.24, h: 0.38, fontFace: 'Arial', fontSize: size, color, margin: 0, fit: 'shrink' });
}
function stat(slide, value, label, x, y, w, opts = {}) {
  slide.addText(value, { x, y, w, h: 0.62, fontFace: 'Arial', fontSize: opts.size || 36, bold: true, color: opts.color || C.green, margin: 0, align: opts.align || 'left', fit: 'shrink' });
  slide.addText(label, { x, y: y + 0.68, w, h: 0.42, fontFace: 'Arial', fontSize: 12, color: opts.labelColor || C.muted, margin: 0, align: opts.align || 'left', fit: 'shrink' });
}
function node(slide, x, y, n, label, fill = C.green) {
  slide.addShape(pptx.ShapeType.ellipse, { x, y, w: 0.62, h: 0.62, fill: { color: fill }, line: { color: fill, transparency: 100 } });
  slide.addText(String(n), { x, y: y + 0.12, w: 0.62, h: 0.24, fontFace: 'Arial', fontSize: 15, bold: true, color: C.white, align: 'center', margin: 0 });
  slide.addText(label, { x: x - 0.15, y: y + 0.78, w: 0.92, h: 0.48, fontFace: 'Arial', fontSize: 11, bold: true, color: C.text, align: 'center', margin: 0, fit: 'shrink' });
}

// 1 Cover
{
  const s = pptx.addSlide('DARK');
  card(s, 6.45, 1.05, 6.2, 4.35, { fill: C.white, transparency: 94, line: C.white, lineTransparency: 90, shadow: false });
  s.addImage({ path: HERO_IMAGE, x: 6.58, y: 1.18, w: 5.94, h: 3.96, altText: 'AI evaluation hub linking candidate models to a to-do workflow, an original vertical shooter and evidence cards.' });
  s.addText('AI VIBE CODING', { x: 0.75, y: 1.08, w: 4.8, h: 0.35, fontFace: 'Arial', fontSize: 15, bold: true, color: 'E9A36F', charSpacing: 2, margin: 0 });
  s.addText('Model Comparison\nEvaluation Report', { x: 0.75, y: 1.62, w: 5.35, h: 1.65, fontFace: 'Arial', fontSize: 39, bold: true, color: C.white, margin: 0, breakLine: false, fit: 'shrink' });
  s.addText('Version 4', { x: 0.75, y: 3.54, w: 2.5, h: 0.45, fontFace: 'Arial', fontSize: 24, bold: true, color: 'B7DCD8', margin: 0 });
  s.addText('Research complete. Controlled and human results intentionally unfilled.', { x: 0.75, y: 4.12, w: 5.4, h: 0.60, fontFace: 'Arial', fontSize: 16, color: 'D7EAE8', margin: 0, fit: 'shrink' });
  pill(s, '3 exact endpoints', 0.75, 5.35, 1.9, 'E7F3F1', C.dark);
  pill(s, '2 complete app workflows', 2.82, 5.35, 2.4, 'FFF2EA', C.orangeDark);
  pill(s, '15 / 55 / 30 evidence model', 5.39, 5.35, 2.7, 'D7EAE8', C.dark);
  s.addText('Prepared for internal model-selection review', { x: 0.75, y: 6.16, w: 6.0, h: 0.35, fontFace: 'Arial', fontSize: 13, color: 'B7DCD8', margin: 0 });
  addSource(s, 'Companion to: ai-vibe-coding-model-comparison-test-report-v4.docx', true);
  s.addNotes('Open with the decision question. This V4 deck is deliberately honest: the methodology and research are complete, but no application-test or human-test winner is invented.');
}

// 2 Agenda
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Deck map', 'The story moves from evidence gaps to an executable decision', 'Four chapters keep the management question visible from start to finish.');
  const chapters = [
    { n: '01', title: 'DECISION STATE', body: 'What V4 can conclude now — and why there is no winner yet.', x: 0.65, y: 2.55, fill: C.dark, color: C.white },
    { n: '02', title: 'RESEARCH FINDINGS', body: 'Exact endpoints, context limits and checkpoint-versus-provider gaps.', x: 6.83, y: 2.55, fill: C.soft, color: C.dark },
    { n: '03', title: 'CONTROLLED EXECUTION', body: 'Two applications, fair controls, run ledger and human evidence.', x: 0.65, y: 4.52, fill: C.orangePale, color: C.dark },
    { n: '04', title: 'DECISION RULE', body: 'Mandatory gates, score weighting, boundaries and next action.', x: 6.83, y: 4.52, fill: C.white, color: C.dark }
  ];
  chapters.forEach((c) => {
    card(s, c.x, c.y, 5.85, 1.55, { fill: c.fill, line: c.fill === C.white ? C.border : c.fill, lineTransparency: c.fill === C.white ? 20 : 100, shadow: c.fill !== C.dark });
    s.addText(c.n, { x: c.x + 0.32, y: c.y + 0.28, w: 0.72, h: 0.40, fontFace: 'Arial', fontSize: 23, bold: true, color: c.fill === C.dark ? 'E9A36F' : C.orangeDark, margin: 0 });
    s.addText(c.title, { x: c.x + 1.25, y: c.y + 0.24, w: 4.15, h: 0.28, fontFace: 'Arial', fontSize: 12, bold: true, color: c.color, charSpacing: 1.0, margin: 0 });
    s.addText(c.body, { x: c.x + 1.25, y: c.y + 0.68, w: 4.15, h: 0.55, fontFace: 'Arial', fontSize: 15, color: c.fill === C.dark ? 'D7EAE8' : C.text, margin: 0, fit: 'shrink' });
  });
  addSource(s, 'Structure follows the V4 report from executive decision through controlled execution and final gate.');
  s.addNotes('Use this map to set expectations: the deck first states the honest decision status, then shows the research, the controlled run design and the rule that will convert evidence into a recommendation.');
}

// 3 Current result
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Executive decision', 'The V4 result: evaluation-ready, not decision-ready', 'The responsible answer before controlled execution is “no winner yet”.');
  card(s, 0.65, 2.52, 5.0, 3.6, { fill: C.dark, line: C.dark });
  s.addText('NO\nWINNER\nYET', { x: 1.05, y: 2.92, w: 3.8, h: 2.2, fontFace: 'Arial', fontSize: 39, bold: true, color: C.white, margin: 0, breakLine: false, fit: 'shrink' });
  s.addText('Missing evidence is not a zero. It is a stop sign.', { x: 1.05, y: 5.36, w: 4.0, h: 0.4, fontFace: 'Arial', fontSize: 13, color: 'B7DCD8', margin: 0 });
  card(s, 6.0, 2.52, 6.65, 1.0, { fill: C.white });
  s.addText('1', { x: 6.35, y: 2.78, w: 0.4, h: 0.35, fontFace: 'Arial', fontSize: 20, bold: true, color: C.orangeDark, margin: 0 });
  s.addText('Freeze exact endpoints, prompts, tools and evidence rules.', { x: 6.9, y: 2.72, w: 5.1, h: 0.42, fontFace: 'Arial', fontSize: 16, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
  card(s, 6.0, 3.78, 6.65, 1.0, { fill: C.white });
  s.addText('2', { x: 6.35, y: 4.04, w: 0.4, h: 0.35, fontFace: 'Arial', fontSize: 20, bold: true, color: C.orangeDark, margin: 0 });
  s.addText('Run To-Do List + vertical shooter three times per endpoint.', { x: 6.9, y: 3.96, w: 5.1, h: 0.48, fontFace: 'Arial', fontSize: 16, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
  card(s, 6.0, 5.04, 6.65, 1.0, { fill: C.white });
  s.addText('3', { x: 6.35, y: 5.30, w: 0.4, h: 0.35, fontFace: 'Arial', fontSize: 20, bold: true, color: C.orangeDark, margin: 0 });
  s.addText('Apply mandatory gates first; rank only complete evidence.', { x: 6.9, y: 5.24, w: 5.1, h: 0.42, fontFace: 'Arial', fontSize: 16, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
  addSource(s, 'V4 report §1 and §14');
  s.addNotes('Emphasise that this is a positive outcome: the evaluation is ready to run and the decision rule is protected from fabricated or incomplete data.');
}

// 3 endpoints
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Candidate set', 'Compare exact endpoints — not family names', 'All facts below are current provider or official model-card facts; none are app-test results.');
  const xs = [0.65, 4.88, 9.11];
  const data = [
    { n: '01', id: 'deepseek-ai/\nDeepSeek-V4-Flash', tag: 'COST-FOCUSED', ctx: '131K endpoint', price: '$0.14 / $0.28', note: 'Text-only endpoint', fill: 'E7F3F1' },
    { n: '02', id: 'deepseek-ai/\nDeepSeek-V4-Pro', tag: 'QUALITY HYPOTHESIS', ctx: '131K endpoint', price: '$0.435 / $0.87', note: 'Text-only endpoint', fill: 'FFF2EA' },
    { n: '03', id: 'Qwen/\nQwen3.5-9B', tag: 'SMALL OPEN-WEIGHT', ctx: '32K endpoint', price: '$0.30 / $0.30', note: 'Weights have vision; endpoint does not', fill: 'FFFFFF' }
  ];
  data.forEach((d, i) => {
    card(s, xs[i], 2.55, 3.58, 3.9, { fill: d.fill, line: C.border, lineTransparency: 25 });
    s.addText(d.n, { x: xs[i] + 0.28, y: 2.83, w: 0.6, h: 0.38, fontFace: 'Arial', fontSize: 20, bold: true, color: C.orangeDark, margin: 0 });
    pill(s, d.tag, xs[i] + 1.35, 2.82, 1.85, C.dark, C.white);
    s.addText(d.id, { x: xs[i] + 0.28, y: 3.45, w: 3.0, h: 0.82, fontFace: 'Arial', fontSize: 18, bold: true, color: C.dark, margin: 0, breakLine: false, fit: 'shrink' });
    stat(s, d.ctx, 'Current provider limit', xs[i] + 0.28, 4.55, 2.95, { size: 24 });
    s.addText(d.price, { x: xs[i] + 0.28, y: 5.45, w: 2.95, h: 0.30, fontFace: 'Arial', fontSize: 15, bold: true, color: C.orangeDark, margin: 0 });
    s.addText('USD / 1M input · output', { x: xs[i] + 0.28, y: 5.78, w: 2.95, h: 0.26, fontFace: 'Arial', fontSize: 10, color: C.muted, margin: 0 });
    s.addText(d.note, { x: xs[i] + 0.28, y: 6.12, w: 2.95, h: 0.26, fontFace: 'Arial', fontSize: 10, bold: true, color: C.text, margin: 0, fit: 'shrink' });
  });
  addSource(s, 'Sources: official DeepSeek/Qwen model cards + authenticated Pioneer /v1/models, captured 2026-08-17');
  s.addNotes('These are the three exact deployable endpoints used by V4. Price figures are list prices, not the final accepted-build cost.');
}

// 4 context gap
{
  const s = pptx.addSlide('DARK');
  addTitle(s, 'Critical research finding', 'Model-card context ≠ provider endpoint context', 'The endpoint limit governs this test. A checkpoint headline does not.', true);
  card(s, 0.7, 2.6, 5.8, 3.55, { fill: 'FFFFFF', transparency: 93, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('DeepSeek V4', { x: 1.05, y: 2.95, w: 2.7, h: 0.42, fontFace: 'Arial', fontSize: 22, bold: true, color: C.white, margin: 0 });
  stat(s, '1M', 'official model card', 1.05, 3.65, 1.8, { color: 'E9A36F', labelColor: 'B7DCD8', size: 38 });
  s.addShape(pptx.ShapeType.chevron, { x: 2.95, y: 3.95, w: 0.8, h: 0.52, fill: { color: 'B7DCD8' }, line: { color: 'B7DCD8', transparency: 100 } });
  stat(s, '131K', 'current endpoint', 4.0, 3.65, 1.85, { color: C.white, labelColor: 'B7DCD8', size: 38 });
  pill(s, 'USE 131K FOR TEST DESIGN', 1.05, 5.25, 4.75, '006A63', C.white);
  card(s, 6.82, 2.6, 5.8, 3.55, { fill: 'FFFFFF', transparency: 93, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('Qwen3.5-9B', { x: 7.17, y: 2.95, w: 2.7, h: 0.42, fontFace: 'Arial', fontSize: 22, bold: true, color: C.white, margin: 0 });
  stat(s, '262K', 'native checkpoint', 7.17, 3.65, 1.8, { color: 'E9A36F', labelColor: 'B7DCD8', size: 38 });
  s.addShape(pptx.ShapeType.chevron, { x: 9.14, y: 3.95, w: 0.8, h: 0.52, fill: { color: 'B7DCD8' }, line: { color: 'B7DCD8', transparency: 100 } });
  stat(s, '32K', 'current endpoint', 10.15, 3.65, 1.65, { color: C.white, labelColor: 'B7DCD8', size: 38 });
  pill(s, 'USE 32K FOR TEST DESIGN', 7.17, 5.25, 4.75, 'E6762D', C.white);
  addSource(s, 'Official model cards + provider catalogue. Qwen can extend to ~1.01M only with special serving configuration.', true);
  s.addNotes('This is the most important research finding. Family or checkpoint capability must not be copied into an endpoint comparison without verification.');
}

// 5 vision gap
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Multimodal reality', 'Vision in the weights does not guarantee vision at the endpoint', 'Use a screenshot canary. Never infer support from the model family.');
  card(s, 0.75, 2.6, 4.7, 3.55, { fill: C.white });
  s.addShape(pptx.ShapeType.rect, { x: 1.25, y: 3.15, w: 1.65, h: 1.25, fill: { color: C.soft }, line: { color: C.green, width: 1.5 } });
  s.addShape(pptx.ShapeType.ellipse, { x: 1.55, y: 3.45, w: 0.28, h: 0.28, fill: { color: C.orange }, line: { color: C.orange, transparency: 100 } });
  s.addShape(pptx.ShapeType.chevron, { x: 3.1, y: 3.47, w: 0.72, h: 0.5, fill: { color: C.green }, line: { color: C.green, transparency: 100 } });
  s.addShape(pptx.ShapeType.ellipse, { x: 4.0, y: 3.15, w: 0.92, h: 0.92, fill: { color: C.dark }, line: { color: C.dark, transparency: 100 } });
  s.addText('AI', { x: 4.0, y: 3.43, w: 0.92, h: 0.24, fontFace: 'Arial', fontSize: 15, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('Checkpoint capability', { x: 1.25, y: 4.78, w: 3.7, h: 0.32, fontFace: 'Arial', fontSize: 17, bold: true, color: C.dark, margin: 0 });
  s.addText('Qwen3.5-9B official weights include a vision encoder.', { x: 1.25, y: 5.2, w: 3.55, h: 0.5, fontFace: 'Arial', fontSize: 14, color: C.text, margin: 0, fit: 'shrink' });
  card(s, 5.82, 2.6, 6.75, 3.55, { fill: C.orangePale, line: C.orangePale });
  s.addShape(pptx.ShapeType.ellipse, { x: 6.35, y: 3.15, w: 1.0, h: 1.0, fill: { color: C.orangeDark }, line: { color: C.orangeDark, transparency: 100 } });
  s.addText('×', { x: 6.35, y: 3.33, w: 1.0, h: 0.42, fontFace: 'Arial', fontSize: 28, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('Current endpoint flags', { x: 7.75, y: 3.08, w: 3.8, h: 0.4, fontFace: 'Arial', fontSize: 22, bold: true, color: C.dark, margin: 0 });
  bullet(s, 'DeepSeek V4 Flash: image input false', 7.75, 3.75, 4.25, C.text, 15);
  bullet(s, 'DeepSeek V4 Pro: image input false', 7.75, 4.3, 4.25, C.text, 15);
  bullet(s, 'Qwen3.5-9B: image input false', 7.75, 4.85, 4.25, C.text, 15);
  pill(s, 'TEXT-ONLY BASELINE FOR V4', 7.75, 5.55, 3.6, C.dark, C.white);
  addSource(s, 'Source: official Qwen3.5-9B model card + provider capability flags, 2026-08-17');
  s.addNotes('The deck separates model capability from service capability. The provider endpoint controls what the test can actually use.');
}

// 6 evaluation architecture
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Evidence design', 'Three layers prevent a benchmark-only decision', 'External evidence informs the test. Controlled delivery and human judgement decide it.');
  const y = 3.05;
  s.addShape(pptx.ShapeType.roundRect, { x: 0.8, y, w: 1.75, h: 1.2, rectRadius: 0.08, fill: { color: C.orange }, line: { color: C.orange, transparency: 100 } });
  s.addText('15%', { x: 0.8, y: y + 0.22, w: 1.75, h: 0.45, fontFace: 'Arial', fontSize: 29, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('External', { x: 0.8, y: y + 0.75, w: 1.75, h: 0.24, fontFace: 'Arial', fontSize: 12, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 2.75, y, w: 6.45, h: 1.2, rectRadius: 0.08, fill: { color: C.green }, line: { color: C.green, transparency: 100 } });
  s.addText('55%', { x: 2.75, y: y + 0.22, w: 6.45, h: 0.45, fontFace: 'Arial', fontSize: 29, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('Controlled application test', { x: 2.75, y: y + 0.75, w: 6.45, h: 0.24, fontFace: 'Arial', fontSize: 12, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addShape(pptx.ShapeType.roundRect, { x: 9.4, y, w: 3.15, h: 1.2, rectRadius: 0.08, fill: { color: C.dark }, line: { color: C.dark, transparency: 100 } });
  s.addText('30%', { x: 9.4, y: y + 0.22, w: 3.15, h: 0.45, fontFace: 'Arial', fontSize: 29, bold: true, color: C.white, align: 'center', margin: 0 });
  s.addText('Human evaluation', { x: 9.4, y: y + 0.75, w: 3.15, h: 0.24, fontFace: 'Arial', fontSize: 12, bold: true, color: C.white, align: 'center', margin: 0 });
  const cards = [
    ['Know the endpoint', 'Model cards · provider limits · price · licence'],
    ['Prove delivery', 'Functions · reliability · time · tokens · accepted cost'],
    ['Judge usability', 'Clarity · fit · trust · recovery · maintainability']
  ];
  [0.8, 4.55, 8.3].forEach((x, i) => {
    card(s, x, 4.75, 3.45, 1.35, { fill: C.white });
    s.addText(cards[i][0], { x: x + 0.25, y: 5.0, w: 2.95, h: 0.30, fontFace: 'Arial', fontSize: 17, bold: true, color: C.dark, margin: 0 });
    s.addText(cards[i][1], { x: x + 0.25, y: 5.42, w: 2.95, h: 0.40, fontFace: 'Arial', fontSize: 12, color: C.muted, margin: 0, fit: 'shrink' });
  });
  addSource(s, 'Internal V4 decision rule; ISO/IEC 25010 informs product-quality coverage but does not prescribe these weights.');
  s.addNotes('The 55% controlled layer is dominant. External scores and model-card claims cannot overwhelm direct app evidence.');
}

// 7 App A
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Application A', 'A familiar business workflow exposes hidden quality gaps', 'The To-Do List makes requirement gaps, validation and persistence easy to verify.');
  const flow = [
    ['Create', 'valid input'], ['Edit', 'all fields'], ['Complete', 'reopen'], ['Filter', 'all / active / done'], ['Persist', 'reload'], ['Verify', 'tests + a11y']
  ];
  const xs = [0.75, 2.8, 4.85, 6.9, 8.95, 11.0];
  flow.forEach((f, i) => {
    if (i < flow.length - 1) s.addShape(pptx.ShapeType.chevron, { x: xs[i] + 1.45, y: 3.45, w: 0.42, h: 0.4, fill: { color: C.border }, line: { color: C.border, transparency: 100 } });
    s.addShape(pptx.ShapeType.ellipse, { x: xs[i], y: 2.9, w: 1.35, h: 1.35, fill: { color: i === 5 ? C.orange : C.green }, line: { color: C.white, width: 2 } });
    s.addText(String(i + 1), { x: xs[i], y: 3.22, w: 1.35, h: 0.28, fontFace: 'Arial', fontSize: 19, bold: true, color: C.white, align: 'center', margin: 0 });
    s.addText(f[0], { x: xs[i] - 0.15, y: 4.48, w: 1.65, h: 0.30, fontFace: 'Arial', fontSize: 15, bold: true, color: C.dark, align: 'center', margin: 0 });
    s.addText(f[1], { x: xs[i] - 0.15, y: 4.84, w: 1.65, h: 0.34, fontFace: 'Arial', fontSize: 10, color: C.muted, align: 'center', margin: 0, fit: 'shrink' });
  });
  card(s, 0.75, 5.55, 12.0, 0.9, { fill: C.dark, line: C.dark });
  s.addText('Acceptance gate', { x: 1.05, y: 5.82, w: 1.7, h: 0.28, fontFace: 'Arial', fontSize: 17, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('All mandatory journeys pass · no critical accessibility issue · no console error · tests pass · evidence complete', { x: 2.85, y: 5.78, w: 9.25, h: 0.35, fontFace: 'Arial', fontSize: 14, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  addSource(s, 'V4 report §7 · WCAG 2.2 · Google Web Vitals');
  s.addNotes('Application A focuses on common business workflow quality: state, validation, persistence, responsive behaviour, accessibility and maintainability.');
}

// 8 App B
{
  const s = pptx.addSlide('DARK');
  addTitle(s, 'Application B', 'The shooter reveals real-time state and regression risk', 'A harder systems test: collision, input, performance and originality.', true);
  // simple plane and enemy field illustration
  s.addShape(pptx.ShapeType.chevron, { x: 1.35, y: 4.75, w: 1.0, h: 1.2, rotate: 270, fill: { color: 'E9A36F' }, line: { color: 'E9A36F', transparency: 100 } });
  for (let i = 0; i < 3; i++) s.addShape(pptx.ShapeType.ellipse, { x: 1.78, y: 4.0 - i * 0.65, w: 0.14, h: 0.34, fill: { color: C.white }, line: { color: C.white, transparency: 100 } });
  const ex = [0.9, 1.9, 2.9, 3.9];
  ex.forEach((x, i) => s.addShape(pptx.ShapeType.hexagon, { x, y: 2.65 + (i % 2) * 0.55, w: 0.62, h: 0.48, fill: { color: i === 3 ? C.orange : C.green }, line: { color: C.white, width: 1 } }));
  card(s, 5.0, 2.6, 3.4, 1.45, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('STATE', { x: 5.35, y: 2.95, w: 1.2, h: 0.3, fontFace: 'Arial', fontSize: 12, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('Stage · boss · pause · restart', { x: 5.35, y: 3.35, w: 2.55, h: 0.35, fontFace: 'Arial', fontSize: 15, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  card(s, 8.65, 2.6, 3.4, 1.45, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('PHYSICS', { x: 9.0, y: 2.95, w: 1.2, h: 0.3, fontFace: 'Arial', fontSize: 12, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('Movement · fire · collision · damage', { x: 9.0, y: 3.35, w: 2.55, h: 0.35, fontFace: 'Arial', fontSize: 15, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  card(s, 5.0, 4.35, 3.4, 1.45, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('RUNTIME', { x: 5.35, y: 4.7, w: 1.2, h: 0.3, fontFace: 'Arial', fontSize: 12, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('FPS · 1% low · 10-minute stability', { x: 5.35, y: 5.1, w: 2.55, h: 0.35, fontFace: 'Arial', fontSize: 15, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  card(s, 8.65, 4.35, 3.4, 1.45, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('ORIGINALITY', { x: 9.0, y: 4.7, w: 1.45, h: 0.3, fontFace: 'Arial', fontSize: 12, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('No copied art · audio · maps · branding', { x: 9.0, y: 5.1, w: 2.55, h: 0.35, fontFace: 'Arial', fontSize: 15, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  addSource(s, 'V4 report §8 · fixed hardware/browser · original assets only', true);
  s.addNotes('Application B is not a screenshot contest. It tests real-time systems, regression risk and runtime stability.');
}

// 9 controls
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Fairness controls', 'Same race. Same track. Same finish line.', 'Only the model endpoint changes between valid runs.');
  const items = [
    ['Prompt', 'Frozen task + acceptance criteria'], ['Repository', 'Equivalent clean starting commit'], ['Harness', 'Same agent, tools and permissions'], ['Environment', 'Same OS, browser and hardware'], ['Limits', '60 min + max two corrections'], ['Evidence', 'Same tests, screenshots and logs']
  ];
  items.forEach((d, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = 0.75 + col * 4.15, y = 2.65 + row * 1.75;
    card(s, x, y, 3.65, 1.35, { fill: i % 2 ? C.white : C.soft, line: C.border, lineTransparency: 40 });
    s.addShape(pptx.ShapeType.ellipse, { x: x + 0.28, y: y + 0.34, w: 0.62, h: 0.62, fill: { color: i === 4 ? C.orange : C.green }, line: { color: C.white, width: 1 } });
    s.addText(String(i + 1), { x: x + 0.28, y: y + 0.49, w: 0.62, h: 0.22, fontFace: 'Arial', fontSize: 13, bold: true, color: C.white, align: 'center', margin: 0 });
    s.addText(d[0], { x: x + 1.12, y: y + 0.28, w: 2.2, h: 0.28, fontFace: 'Arial', fontSize: 17, bold: true, color: C.dark, margin: 0 });
    s.addText(d[1], { x: x + 1.12, y: y + 0.66, w: 2.15, h: 0.40, fontFace: 'Arial', fontSize: 11, color: C.muted, margin: 0, fit: 'shrink' });
  });
  card(s, 0.75, 6.18, 12.0, 0.55, { fill: C.orangePale, line: C.orangePale, shadow: false });
  s.addText('Invalid run ≠ bad model run. Preserve the evidence and classify model, provider, infrastructure or tester cause.', { x: 1.05, y: 6.34, w: 11.35, h: 0.24, fontFace: 'Arial', fontSize: 13, bold: true, color: C.orangeDark, align: 'center', margin: 0, fit: 'shrink' });
  addSource(s, 'V4 report §5');
  s.addNotes('A fair test freezes the complete execution system. Differences in model family do not justify different prompts, correction budgets or evidence standards.');
}

// 10 sprint
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Execution plan', 'Two developers. Five days. No model ownership bias.', 'Each developer owns an application and tests every candidate.');
  const days = [
    ['1', 'FREEZE', 'prompts · repos · limits'], ['2', 'BLIND RUNS', 'first builds · raw logs'], ['3', 'REPEAT + FIX', '3 runs · correction rounds'], ['4', 'HUMAN REVIEW', 'cross-review · interviews'], ['5', 'DECIDE', 'evidence · gates · recommendation']
  ];
  days.forEach((d, i) => {
    const x = 0.72 + i * 2.5;
    if (i < 4) s.addShape(pptx.ShapeType.chevron, { x: x + 1.92, y: 3.72, w: 0.38, h: 0.42, fill: { color: C.border }, line: { color: C.border, transparency: 100 } });
    s.addShape(pptx.ShapeType.ellipse, { x, y: 3.15, w: 1.4, h: 1.4, fill: { color: i === 4 ? C.orange : C.green }, line: { color: C.white, width: 2 } });
    s.addText(d[0], { x, y: 3.46, w: 1.4, h: 0.42, fontFace: 'Arial', fontSize: 27, bold: true, color: C.white, align: 'center', margin: 0 });
    s.addText(d[1], { x: x - 0.25, y: 4.82, w: 1.9, h: 0.30, fontFace: 'Arial', fontSize: 13, bold: true, color: C.dark, align: 'center', margin: 0, fit: 'shrink' });
    s.addText(d[2], { x: x - 0.25, y: 5.18, w: 1.9, h: 0.46, fontFace: 'Arial', fontSize: 10, color: C.muted, align: 'center', margin: 0, fit: 'shrink' });
  });
  card(s, 0.75, 6.05, 5.8, 0.7, { fill: C.dark, line: C.dark, shadow: false });
  s.addText('Developer 1', { x: 1.05, y: 6.25, w: 1.3, h: 0.26, fontFace: 'Arial', fontSize: 14, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('owns App A · cross-reviews App B', { x: 2.4, y: 6.25, w: 3.65, h: 0.26, fontFace: 'Arial', fontSize: 13, color: C.white, margin: 0 });
  card(s, 6.75, 6.05, 5.8, 0.7, { fill: C.dark, line: C.dark, shadow: false });
  s.addText('Developer 2', { x: 7.05, y: 6.25, w: 1.3, h: 0.26, fontFace: 'Arial', fontSize: 14, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('owns App B · cross-reviews App A', { x: 8.4, y: 6.25, w: 3.65, h: 0.26, fontFace: 'Arial', fontSize: 13, color: C.white, margin: 0 });
  addSource(s, 'V4 report §6');
  s.addNotes('Applications are assigned to developers, not models. This reduces model-specific coaching or familiarity bias.');
}

// 11 token accounting
{
  const s = pptx.addSlide('DARK');
  addTitle(s, 'Run economics', 'Token accounting starts at the run — not the summary', 'Preserve provider-native fields before calculating comparable totals.', true);
  const labels = ['Prompt', 'Correction', 'Cache', 'Output', 'Reasoning', 'Image', 'Provider total', 'Cost'];
  labels.forEach((l, i) => {
    const x = 0.7 + i * 1.55;
    s.addShape(pptx.ShapeType.roundRect, { x, y: 2.8, w: 1.28, h: 0.95, rectRadius: 0.06, fill: { color: i === 7 ? C.orange : 'FFFFFF', transparency: i === 7 ? 0 : 91 }, line: { color: i === 7 ? C.orange : 'FFFFFF', transparency: 100 } });
    s.addText(l, { x: x + 0.1, y: 3.11, w: 1.08, h: 0.28, fontFace: 'Arial', fontSize: 12, bold: true, color: C.white, align: 'center', margin: 0, fit: 'shrink' });
    if (i < labels.length - 1) s.addShape(pptx.ShapeType.chevron, { x: x + 1.30, y: 3.08, w: 0.22, h: 0.36, fill: { color: 'B7DCD8' }, line: { color: 'B7DCD8', transparency: 100 } });
  });
  card(s, 0.75, 4.25, 3.65, 1.55, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  stat(s, 'A', 'App A', 1.05, 4.55, 0.65, { color: 'E9A36F', labelColor: 'B7DCD8', size: 34 });
  s.addText('Tokens · cost · accepted builds\nper-success efficiency', { x: 1.8, y: 4.55, w: 2.15, h: 0.7, fontFace: 'Arial', fontSize: 14, bold: true, color: C.white, margin: 0, breakLine: false, fit: 'shrink' });
  card(s, 4.82, 4.25, 3.65, 1.55, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  stat(s, 'B', 'App B', 5.12, 4.55, 0.65, { color: 'E9A36F', labelColor: 'B7DCD8', size: 34 });
  s.addText('Tokens · cost · accepted builds\nper-success efficiency', { x: 5.87, y: 4.55, w: 2.15, h: 0.7, fontFace: 'Arial', fontSize: 14, bold: true, color: C.white, margin: 0, breakLine: false, fit: 'shrink' });
  card(s, 8.89, 4.25, 3.65, 1.55, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  stat(s, 'Σ', 'A + B', 9.19, 4.55, 0.65, { color: 'E9A36F', labelColor: 'B7DCD8', size: 34 });
  s.addText('Keep A + B visible\nNever publish only one total', { x: 9.94, y: 4.55, w: 2.15, h: 0.7, fontFace: 'Arial', fontSize: 14, bold: true, color: C.white, margin: 0, breakLine: false, fit: 'shrink' });
  s.addText('Reasoning may already be included in output. Image tokens may be unreported. Subscription cost is not API token cost.', { x: 0.85, y: 6.3, w: 11.8, h: 0.34, fontFace: 'Arial', fontSize: 13, bold: true, color: 'D7EAE8', align: 'center', margin: 0, fit: 'shrink' });
  addSource(s, 'V4 report §10–12', true);
  s.addNotes('The report includes 18 run rows plus separate App A, App B and combined aggregates. Provider-native fields are preserved to avoid double-counting.');
}

// 12 expected actual
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Evidence discipline', 'Expected is frozen. Actual is observed.', 'A result is not a restatement of the requirement. It is an evidence-backed observation.');
  card(s, 0.75, 2.7, 5.65, 3.25, { fill: C.soft, line: C.soft });
  pill(s, 'BEFORE THE RUN', 1.1, 3.05, 1.7, C.green, C.white);
  s.addText('EXPECTED', { x: 1.1, y: 3.68, w: 2.5, h: 0.48, fontFace: 'Arial', fontSize: 29, bold: true, color: C.dark, margin: 0 });
  bullet(s, 'Requirement ID', 1.1, 4.35, 4.4, C.text, 15);
  bullet(s, 'Verifiable acceptance outcome', 1.1, 4.82, 4.4, C.text, 15);
  bullet(s, 'Mandatory or optional gate', 1.1, 5.29, 4.4, C.text, 15);
  s.addShape(pptx.ShapeType.chevron, { x: 6.52, y: 3.92, w: 0.55, h: 0.72, fill: { color: C.orange }, line: { color: C.orange, transparency: 100 } });
  card(s, 7.18, 2.7, 5.4, 3.25, { fill: C.white });
  pill(s, 'AFTER THE RUN', 7.53, 3.05, 1.7, C.orange, C.white);
  s.addText('ACTUAL', { x: 7.53, y: 3.68, w: 2.5, h: 0.48, fontFace: 'Arial', fontSize: 29, bold: true, color: C.dark, margin: 0 });
  bullet(s, 'Pass / Partial / Fail / Invalid', 7.53, 4.35, 4.4, C.text, 15);
  bullet(s, 'Observed behaviour + severity', 7.53, 4.82, 4.4, C.text, 15);
  bullet(s, 'Test, screenshot, log or video', 7.53, 5.29, 4.4, C.text, 15);
  s.addText('Missing data remains “Not yet measured” — never 0.', { x: 2.1, y: 6.35, w: 9.1, h: 0.34, fontFace: 'Arial', fontSize: 15, bold: true, color: C.orangeDark, align: 'center', margin: 0 });
  addSource(s, 'V4 report §7–9');
  s.addNotes('This is the answer to the original gap: V4 provides expected, actual and evidence fields for every acceptance item, plus run-level and aggregate measurement ledgers.');
}

// 13 human evaluation
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Human evidence', 'Ten questions — but one complete workflow', 'Interviews support the case study. They do not replace the build, test and correction journey.');
  const groups = [
    ['USE', 'Can users complete the task?', 'First-use clarity · controls · mobile'],
    ['TRUST', 'Do errors and state changes make sense?', 'Validation · deletion · pause · restart'],
    ['FIT', 'Does the build match requirements?', 'Missing features · expectation gaps'],
    ['MAINTAIN', 'Would engineers continue this codebase?', 'Structure · tests · documentation']
  ];
  groups.forEach((g, i) => {
    const x = 0.75 + i * 3.05;
    card(s, x, 2.75, 2.65, 2.6, { fill: i % 2 ? C.white : C.soft, line: C.border, lineTransparency: 45 });
    pill(s, g[0], x + 0.3, 3.08, 1.0, i === 1 ? C.orange : C.green, C.white);
    s.addText(g[1], { x: x + 0.3, y: 3.65, w: 2.05, h: 0.72, fontFace: 'Arial', fontSize: 18, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
    s.addText(g[2], { x: x + 0.3, y: 4.58, w: 2.05, h: 0.46, fontFace: 'Arial', fontSize: 11, color: C.muted, margin: 0, fit: 'shrink' });
  });
  card(s, 0.75, 5.75, 11.85, 0.75, { fill: C.dark, line: C.dark, shadow: false });
  s.addText('Rubric anchors', { x: 1.05, y: 5.99, w: 1.6, h: 0.28, fontFace: 'Arial', fontSize: 16, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('1 = cannot complete / unsafe     3 = works with friction     5 = clear, efficient and maintainable', { x: 2.85, y: 5.99, w: 8.95, h: 0.28, fontFace: 'Arial', fontSize: 14, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  addSource(s, 'V4 report §13');
  s.addNotes('Anonymise builds where practical. Every rating needs a factual observation and reviewers should record disagreement rather than force consensus.');
}

// 14 scoring
{
  const s = pptx.addSlide('DARK');
  addTitle(s, 'Decision logic', 'Pass the gate. Then calculate the score.', 'A high average cannot rescue a broken or unsafe accepted build.', true);
  card(s, 0.75, 2.65, 4.2, 3.4, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('MANDATORY GATE', { x: 1.1, y: 3.02, w: 2.9, h: 0.34, fontFace: 'Arial', fontSize: 15, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('PASS', { x: 1.1, y: 3.55, w: 2.6, h: 0.68, fontFace: 'Arial', fontSize: 42, bold: true, color: C.white, margin: 0 });
  bullet(s, 'All mandatory requirements', 1.1, 4.48, 3.25, C.white, 14);
  bullet(s, 'No unresolved S1 / S2', 1.1, 4.92, 3.25, C.white, 14);
  bullet(s, 'No secret or unlicensed asset', 1.1, 5.36, 3.25, C.white, 14);
  s.addShape(pptx.ShapeType.chevron, { x: 5.22, y: 3.75, w: 0.78, h: 0.82, fill: { color: 'B7DCD8' }, line: { color: 'B7DCD8', transparency: 100 } });
  card(s, 6.28, 2.65, 6.3, 3.4, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
  s.addText('WEIGHTED SCORE', { x: 6.65, y: 3.02, w: 2.9, h: 0.34, fontFace: 'Arial', fontSize: 15, bold: true, color: 'E9A36F', margin: 0 });
  s.addText('0.15 External', { x: 6.65, y: 3.62, w: 2.3, h: 0.42, fontFace: 'Arial', fontSize: 24, bold: true, color: C.white, margin: 0 });
  s.addText('+', { x: 9.05, y: 3.62, w: 0.4, h: 0.42, fontFace: 'Arial', fontSize: 24, bold: true, color: 'B7DCD8', margin: 0 });
  s.addText('0.55 Controlled', { x: 9.45, y: 3.62, w: 2.6, h: 0.42, fontFace: 'Arial', fontSize: 24, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  s.addText('+ 0.30 Human', { x: 8.15, y: 4.38, w: 2.8, h: 0.42, fontFace: 'Arial', fontSize: 24, bold: true, color: C.white, margin: 0 });
  pill(s, 'TIE: accepted rate → assistance → cost', 7.12, 5.28, 4.65, C.orange, C.white);
  addSource(s, 'V4 report §14 · missing evidence is not rankable', true);
  s.addNotes('Apply mandatory gates before scoring. For ties, prefer accepted-build rate, then lower human assistance, then lower cost per accepted build.');
}

// 15 limitations
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Decision boundaries', 'What V4 can say — and what it cannot', 'The limitation section is part of the decision, not a disclaimer.');
  card(s, 0.75, 2.7, 5.75, 3.55, { fill: C.soft, line: C.soft });
  pill(s, 'CAN SUPPORT', 1.1, 3.05, 1.6, C.green, C.white);
  bullet(s, 'Best endpoint for these two apps', 1.1, 3.72, 4.75, C.text, 16);
  bullet(s, 'Under the frozen harness and date', 1.1, 4.28, 4.75, C.text, 16);
  bullet(s, 'Accepted-build time, tokens and cost', 1.1, 4.84, 4.75, C.text, 16);
  bullet(s, 'Observed human usability and maintainability', 1.1, 5.40, 4.75, C.text, 16);
  card(s, 6.82, 2.7, 5.75, 3.55, { fill: C.orangePale, line: C.orangePale });
  pill(s, 'CANNOT SUPPORT', 7.17, 3.05, 1.8, C.orangeDark, C.white);
  bullet(s, 'Best coding model in general', 7.17, 3.72, 4.75, C.text, 16);
  bullet(s, 'Production security certification', 7.17, 4.28, 4.75, C.text, 16);
  bullet(s, '1M endpoint context without verification', 7.17, 4.84, 4.75, C.text, 16);
  bullet(s, 'Direct API-vs-local cost equivalence', 7.17, 5.40, 4.75, C.text, 16);
  addSource(s, 'V4 report §15');
  s.addNotes('The most important boundary is endpoint-specificity. Results do not automatically transfer to another provider, reasoning mode, context limit or model version.');
}

// 16 case study
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Case study', 'A business question becomes one traceable evidence journey', 'Not six disconnected demos. Not ten interview answers. One controlled path to a decision.');
  const stages = ['Question', 'Research', 'Freeze', 'Build', 'Correct', 'Validate', 'Human test', 'Measure', 'Limit', 'Decide'];
  stages.forEach((l, i) => {
    const x = 0.65 + (i % 5) * 2.53;
    const y = 2.65 + Math.floor(i / 5) * 1.75;
    if (i % 5 < 4) s.addShape(pptx.ShapeType.chevron, { x: x + 1.9, y: y + 0.38, w: 0.32, h: 0.38, fill: { color: C.border }, line: { color: C.border, transparency: 100 } });
    s.addShape(pptx.ShapeType.ellipse, { x, y, w: 0.95, h: 0.95, fill: { color: i < 3 || i === 8 ? C.green : (i === 9 ? C.orange : C.dark) }, line: { color: C.white, width: 1.5 } });
    s.addText(String(i + 1), { x, y: y + 0.25, w: 0.95, h: 0.26, fontFace: 'Arial', fontSize: 16, bold: true, color: C.white, align: 'center', margin: 0 });
    s.addText(l, { x: x + 1.05, y: y + 0.22, w: 1.25, h: 0.42, fontFace: 'Arial', fontSize: 14, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
  });
  card(s, 0.75, 6.15, 12.0, 0.58, { fill: C.dark, line: C.dark, shadow: false });
  s.addText('Q&A is evidence inside Stage 7. It is not the case study.', { x: 1.0, y: 6.32, w: 11.5, h: 0.26, fontFace: 'Arial', fontSize: 14, bold: true, color: C.white, align: 'center', margin: 0 });
  addSource(s, 'V4 report §16');
  s.addNotes('The case study traces the business question through research, frozen requirements, runs, correction, validation, human evaluation, economics, limitations and decision.');
}

// 17 close
{
  const s = pptx.addSlide('DARK');
  addTitle(s, 'Next action', 'Run the evidence pack. Then choose.', 'V4 makes the decision reproducible — and makes unsupported confidence visible.', true);
  const steps = [
    ['01', 'Reconfirm endpoint metadata', 'IDs · limits · capability flags · prices'],
    ['02', 'Execute 18 controlled runs', '3 endpoints × 2 apps × 3 runs'],
    ['03', 'Collect human evidence', 'anonymised cross-review + anchored rubric'],
    ['04', 'Apply gates and score', '15 / 55 / 30 + accepted-build efficiency']
  ];
  steps.forEach((d, i) => {
    const x = 0.75 + i * 3.08;
    card(s, x, 2.65, 2.68, 2.6, { fill: 'FFFFFF', transparency: 92, line: 'FFFFFF', lineTransparency: 100, shadow: false });
    s.addText(d[0], { x: x + 0.28, y: 2.96, w: 0.58, h: 0.34, fontFace: 'Arial', fontSize: 18, bold: true, color: 'E9A36F', margin: 0 });
    s.addText(d[1], { x: x + 0.28, y: 3.55, w: 2.08, h: 0.62, fontFace: 'Arial', fontSize: 18, bold: true, color: C.white, margin: 0, fit: 'shrink' });
    s.addText(d[2], { x: x + 0.28, y: 4.45, w: 2.08, h: 0.42, fontFace: 'Arial', fontSize: 11, color: 'B7DCD8', margin: 0, fit: 'shrink' });
  });
  pill(s, 'DECISION STATUS · PENDING MEASURED EVIDENCE', 3.55, 5.72, 6.2, C.orange, C.white);
  s.addText('Report + deck + reproducible generators are versioned in the repository.', { x: 2.2, y: 6.35, w: 8.9, h: 0.35, fontFace: 'Arial', fontSize: 14, color: 'D7EAE8', align: 'center', margin: 0 });
  addSource(s, 'Primary document: docs/reports/ai-vibe-coding-model-comparison-test-report-v4.docx', true);
  s.addNotes('Close by requesting approval to run the frozen evidence pack. The next decision should be based on measured accepted-build evidence, not model naming or benchmark familiarity.');
}

// 18 sources
{
  const s = pptx.addSlide('LIGHT');
  addTitle(s, 'Appendix', 'Research sources', 'Official model cards, provider metadata and current quality standards.');
  const left = [
    ['DeepSeek V4 Flash', 'huggingface.co/deepseek-ai/DeepSeek-V4-Flash'],
    ['DeepSeek V4 Pro', 'huggingface.co/deepseek-ai/DeepSeek-V4-Pro'],
    ['Qwen3.5-9B', 'huggingface.co/Qwen/Qwen3.5-9B'],
    ['Qwen3.5-35B-A3B', 'huggingface.co/Qwen/Qwen3.5-35B-A3B'],
    ['Provider catalogue', 'api.pioneer.ai/v1/models · authenticated capture']
  ];
  const right = [
    ['ISO/IEC 25010:2023', 'iso.org/standard/78176.html'],
    ['WCAG 2.2', 'w3.org/TR/WCAG22/'],
    ['Google Web Vitals', 'web.dev/articles/vitals'],
    ['OWASP ASVS 5.0.0', 'owasp.org/www-project-application-security-verification-standard/'],
    ['Full citations', 'V4 report §18 · accessed 2026-08-17']
  ];
  [left, right].forEach((arr, col) => {
    arr.forEach((d, i) => {
      const x = 0.75 + col * 6.2, y = 2.55 + i * 0.78;
      card(s, x, y, 5.65, 0.62, { fill: i % 2 ? C.white : C.soft, line: C.border, lineTransparency: 65, shadow: false });
      s.addText(d[0], { x: x + 0.22, y: y + 0.12, w: 2.1, h: 0.22, fontFace: 'Arial', fontSize: 12, bold: true, color: C.dark, margin: 0, fit: 'shrink' });
      s.addText(d[1], { x: x + 2.4, y: y + 0.12, w: 3.0, h: 0.22, fontFace: 'Arial', fontSize: 9, color: C.muted, margin: 0, fit: 'shrink' });
    });
  });
  card(s, 0.75, 6.62, 11.85, 0.35, { fill: C.orangePale, line: C.orangePale, shadow: false });
  s.addText('No simulated V3 score, test pass rate, elapsed time, token total, cost or user quote is carried into V4.', { x: 1.0, y: 6.71, w: 11.35, h: 0.18, fontFace: 'Arial', fontSize: 11, bold: true, color: C.orangeDark, align: 'center', margin: 0 });
  addSource(s, 'Access date: 2026-08-17');
  s.addNotes('All external facts in the deck are traceable to the V4 report source list. The authenticated provider catalogue is cited as a dated redacted capture.');
}

const out = path.join(__dirname, '..', '..', 'docs', 'reports', 'ai-vibe-coding-model-comparison-v4-deck.pptx');
(async () => {
  await pptx.writeFile({ fileName: out });
  console.log(out);
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
