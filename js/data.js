/* ==========================================================================
   Machinery Warehouse Outlet — Data Layer
   Model codes, working widths, categories, contact details and company
   facts come from the company's own product documentation. No prices,
   certifications, customer counts or other unverified claims have been
   invented. The "description" field on each product is written by us to
   explain what the listed features mean for a buyer — it does not add any
   spec, number or claim beyond what the company's own documentation already states.
   To add a new machine, add an object to PRODUCTS following the same shape.
   ========================================================================== */

const COMPANY = {
  name: "Machinery Warehouse Outlet",
  shortName: "MWO",
  tagline: "Home of Industrial Machines and Spare Parts",
  quality: "Quality Guaranteed",
  disclaimer:
    "Pictures of our machines may slightly differ from the physical unit, but the quality and specifications are the same.",
  address: "Awada Industrial Zone, 2 Ichi Street, Off Ezeiweka Road, Awada-Obosi, Anambra State",
  phones: ["08033100374", "09095555222"],
  emails: ["machines.warehouse@juninet.com", "machines.warehouse@gmail.com"],
  // International format (no leading +, no leading 0) — used directly to build wa.me links.
  whatsapp: "2349022330011",
  whatsappDisplay: "0902 233 0011",
  socials: {
    facebook: "",
    instagram: "",
  },
};

const CATEGORIES = [
  {
    slug: "film-blowing",
    name: "Film Blowing Machines",
    short: "Film Blowing",
    image: "cat-film-blowing",
    blurb: "Co-extrusion, mono-layer and high-speed HD/LDPE/LLDPE film blowing towers.",
  },
  {
    slug: "bag-making",
    name: "Bag Making Machines",
    short: "Bag Making",
    image: "cat-bag-making",
    blurb: "Multi-line mechanical bag making machines with auto conveyor.",
  },
  {
    slug: "water-packaging",
    name: "Water Packaging Machines",
    short: "Water Packaging",
    image: "prod-sachet-water",
    blurb: "Sachet water filling, sealing and packing machines.",
  },
  {
    slug: "recycling",
    name: "Recycling & Pelletizing",
    short: "Recycling",
    image: "cat-recycling",
    blurb: "Complete recycle pelletizing lines, granulators and grinding machines.",
  },
  {
    slug: "printing",
    name: "Printing Machines",
    short: "Printing",
    image: "cat-printing",
    blurb: "Flexo printing series and gravure printing machines.",
  },
  {
    slug: "moulding",
    name: "Blow & Injection Moulding",
    short: "Moulding",
    image: "cat-moulding",
    blurb: "Blow moulding machines, plastic injection moulding machines, accessories and moulds.",
  },
  {
    slug: "punching",
    name: "Punching Machines",
    short: "Punching",
    image: "cat-punching",
    blurb: "Mechanical and hydraulic punching machines.",
  },
];

/* models: working width / capacity ranges exactly as supplied by the company.
   description: written by us to explain the listed features — not a new claim. */
const PRODUCTS = [
  {
    slug: "ibc-rotary-film-blowing-machine",
    name: "Three-Layer Co-Extrusion IBC Haul-Off Rotary Film Blowing Machine",
    category: "film-blowing",
    image: "prod-ibc-tower",
    gallery: ["prod-ibc-tower"],
    features: ["Three-layer co-extrusion", "Internal Bubble Cooling (IBC)", "Rotary haul-off"],
    description:
      "Three independent layers let you blend materials for strength, clarity or cost in a single pass, while Internal Bubble Cooling and the rotary haul-off work together to keep the bubble stable and the finished film free of wrinkle lines. A strong choice for producers who need consistent gauge across long runs. Offered across three working-width ranges so you can match the tower to your output target.",
    models: [
      { code: "3MW-50", spec: "800–1500mm" },
      { code: "3MW-55", spec: "1200–2000mm" },
      { code: "3MW-65", spec: "1600–2500mm" },
    ],
  },
  {
    slug: "pp-blown-film-machine",
    name: "PP Blown Film Machine",
    category: "film-blowing",
    image: "prod-pp-blown",
    gallery: ["prod-pp-blown"],
    features: [],
    description:
      "Purpose-built for polypropylene rather than adapted from a PE line, giving cleaner results for producers moving into stiffer, higher-clarity PP film. Three working-width options cover light packaging film through wider industrial rolls without changing machine families.",
    models: [
      { code: "MW-PP 45", spec: "100–500mm" },
      { code: "MW-PP 55", spec: "150–600mm" },
      { code: "MW-PP 65", spec: "200–800mm" },
    ],
  },
  {
    slug: "double-colour-film-blowing-machine",
    name: "Double-Colour Film Blowing Machine",
    category: "film-blowing",
    image: "prod-double-colour",
    gallery: ["prod-double-colour"],
    features: [],
    description:
      "Produces two-colour striped film directly during extrusion, so branded or striped packaging film doesn't need a separate printing pass. Available in 500mm and 600mm working widths.",
    models: [
      { code: "MW-40Dx2x500", spec: "500mm" },
      { code: "MW-40Dx2x600", spec: "600mm" },
    ],
  },
  {
    slug: "single-screw-double-die-film-blowing-machine",
    name: "Single-Screw Double-Die Film Blowing Machine",
    category: "film-blowing",
    image: "prod-single-screw",
    gallery: ["prod-single-screw"],
    features: [],
    description:
      "Two dies run from the machine's screw line, so you can produce two film jobs side by side or push more volume of a single spec through one footprint. It is a practical step up for an operation outgrowing a single-line setup.",
    models: [
      { code: "MW-60", spec: "100–500mm" },
      { code: "MW-70", spec: "100–600mm" },
    ],
  },
  {
    slug: "hd-ldpe-lldpe-film-blowing-machine",
    name: "High-Speed HD/LDPE/LLDPE Film Blowing Machine",
    category: "film-blowing",
    image: "prod-hd-ldpe",
    gallery: ["prod-hd-ldpe"],
    features: [],
    description:
      "Runs HD, LDPE and LLDPE resins on the same tower, giving producers who serve more than one film market the flexibility to switch material without switching machines. Three working-width tiers scale from light-gauge bags to wider industrial film.",
    models: [
      { code: "MW-A50", spec: "300–600mm" },
      { code: "MW-A55", spec: "400–800mm" },
      { code: "MW-A65", spec: "800–1200mm" },
    ],
  },
  {
    slug: "rotary-die-head-film-blowing-machine",
    name: "Double Layer Coextrusion Rotary Die Head Film Blowing Machine",
    category: "film-blowing",
    image: "prod-rotary-die",
    gallery: ["prod-rotary-die"],
    features: ["Double layer coextrusion", "Rotary die head"],
    description:
      "The rotary die head turns the bubble evenly as it forms, helping distribute gauge more consistently around the full circumference of the film, a detail that matters when customers inspect for even thickness.",
    models: [],
  },
  {
    slug: "sachet-water-filling-sealing-packing-machine",
    name: "Sachet Water Filling, Sealing and Packing Machine",
    category: "water-packaging",
    image: "prod-sachet-water",
    gallery: ["prod-sachet-water"],
    features: ["Filling", "Sealing", "Packing"],
    description:
      "Fills, seals and packs sachet water in one continuous cycle, the standard production line for pure water producers supplying local and regional markets, built to run consistently shift after shift.",
    models: [],
  },
  {
    slug: "four-lines-bag-making-machine",
    name: "Double Layer Mechanical Four Lines Bag Making Machine with Auto Conveyor",
    category: "bag-making",
    image: "prod-bag-4line",
    gallery: ["prod-bag-4line"],
    features: ["Four lines", "Auto conveyor"],
    description:
      "Four lines and an auto conveyor move finished bags off the machine with minimal manual handling, in working widths from 550mm to 950mm, a solid entry point for producers scaling up from a single-line setup.",
    models: [
      { code: "MW4-B600", spec: "550mm" },
      { code: "MW4-B800", spec: "750mm" },
      { code: "MW4-B1000", spec: "950mm" },
    ],
  },
  {
    slug: "six-lines-bag-making-machine",
    name: "Double Layer Mechanical Six Lines Bag Making Machine with Auto Conveyor",
    category: "bag-making",
    image: "prod-bag-6line",
    gallery: ["prod-bag-6line"],
    features: ["Six lines", "Auto conveyor"],
    description:
      "Six lines with auto conveyor for producers who've outgrown a four-line machine and need more bags per shift without adding a second machine's footprint. Working widths from 850mm to 1000mm.",
    models: [
      { code: "MW6-B900", spec: "850mm" },
      { code: "MW6-B1100", spec: "900mm" },
      { code: "MW6-B1200", spec: "1000mm" },
    ],
  },
  {
    slug: "eight-lines-bag-making-machine",
    name: "Double Layer Eight Lines Bag Making Machine with Auto Conveyor",
    category: "bag-making",
    image: "prod-bag-8line",
    gallery: ["prod-bag-8line"],
    features: ["Eight lines", "Auto conveyor"],
    description:
      "The highest-capacity bag-making line in the range. Eight lines with auto conveyor are built for producers who need to move serious daily volume through a single machine rather than running multiple smaller lines in parallel.",
    models: [
      { code: "MW6-B650", spec: "650mm" },
      { code: "MW6-B850", spec: "850mm" },
      { code: "MW6-B1000", spec: "1000mm" },
    ],
  },
  {
    slug: "complete-pe-pp-recycle-pelletizing-line",
    name: "Complete PE/PP Recycle Pelletizing Line",
    category: "recycling",
    image: "prod-recycle-line",
    gallery: ["prod-recycle-line"],
    features: [],
    description:
      "A full line from conveyor feed through crushing and extrusion, turning PE/PP waste film back into usable pellets. Lets a producer recover value from scrap material instead of paying to have it hauled away.",
    models: [],
  },
  {
    slug: "double-stage-recycle-pelletizing-machine",
    name: "Double Stage Recycle/Pelletizing Machine",
    category: "recycling",
    image: "prod-recycle-stage-double",
    gallery: ["prod-recycle-stage-double"],
    features: [],
    description:
      "A second extrusion stage filters and re-melts the material after the first pass, giving cleaner and more consistent pellets from mixed or lower-grade waste film than a single-stage machine typically produces. Available in 90, 110 and 120 sizes.",
    models: [{ code: "90" }, { code: "110" }, { code: "120" }],
  },
  {
    slug: "single-stage-recycle-pelletizing-machine",
    name: "Single Stage Recycle/Pelletizing Machine",
    category: "recycling",
    image: "prod-recycle-stage-single",
    gallery: ["prod-recycle-stage-single"],
    features: [],
    description:
      "A simpler, single-pass pelletizing line for producers working with cleaner waste streams where a second extrusion stage isn't necessary, which means lower cost and less complexity where the input material doesn't need it. Available in 90, 110 and 120 sizes.",
    models: [{ code: "90" }, { code: "110" }, { code: "120" }],
  },
  {
    slug: "waste-film-granulating-machine",
    name: "Waste Film Granulating Machine",
    category: "recycling",
    image: "prod-waste-granulate",
    gallery: ["prod-waste-granulate"],
    features: [],
    description:
      "Reduces waste film to granulate ready for re-extrusion or pelletizing, in 150L and 300L capacities, a practical first processing step for producers handling their own scrap in-house.",
    models: [{ code: "150L" }, { code: "300L" }],
  },
  {
    slug: "waste-film-grinding-machine",
    name: "Waste Film Grinding Machine",
    category: "recycling",
    image: "prod-waste-grind",
    gallery: ["prod-waste-grind"],
    features: [],
    description:
      "Grinds waste film and production offcuts down to a size suitable for recycling or re-extrusion. Offered in F150, F300 and F500 capacities to match your scrap volume.",
    models: [{ code: "F150" }, { code: "F300" }, { code: "F500" }],
  },
  {
    slug: "mechanical-punching-machine",
    name: "Mechanical Punching Machine",
    category: "punching",
    image: "prod-mech-punch",
    gallery: ["prod-mech-punch"],
    features: [],
    description:
      "A mechanical press for die-cutting and punching across bag, fabric and packaging production. It is straightforward to operate and maintain, and a dependable addition to a finishing line.",
    models: [],
  },
  {
    slug: "hydraulic-punching-machine",
    name: "Hydraulic Punching Machine",
    category: "punching",
    image: "prod-hyd-punch",
    gallery: ["prod-hyd-punch"],
    features: [],
    description:
      "Hydraulic power gives finer control over punching force than a mechanical press, which helps producers hold consistent, repeatable cuts across a full shift of running.",
    models: [],
  },
  {
    slug: "flexo-printing-machine-series",
    name: "Flexo Printing Machine Series",
    category: "printing",
    image: "prod-flexo",
    gallery: ["prod-flexo"],
    features: ["Two-colour", "Four-colour", "Six-colour", "Flexo plate making machine"],
    description:
      "Two, four and six-colour configurations, plus a dedicated flexo plate-making machine, mean you can match your print investment to your current order book and add colour stations later as demand grows, without replacing the whole line.",
    models: [],
  },
  {
    slug: "six-colour-gravure-printing-machine",
    name: "Six-Colour Gravure Printing Machine",
    category: "printing",
    image: "prod-gravure6",
    gallery: ["prod-gravure6"],
    features: [],
    description:
      "Six-colour gravure printing for producers who need sharp, high-repeat print quality on film, well suited to branded packaging that has to look consistent from the first roll to the last.",
    models: [],
  },
  {
    slug: "high-speed-computer-gravure-printing-machine",
    name: "High-Speed Computer Gravure Printing Machine",
    category: "printing",
    image: "prod-comp-gravure",
    gallery: ["prod-comp-gravure"],
    features: [],
    description:
      "Computer-assisted control keeps registration accurate at higher running speeds, aimed at producers printing longer runs where consistency from the first metre to the last matters as much as line speed.",
    models: [],
  },
  {
    slug: "blow-moulding-machine",
    name: "Automatic, Semi-Automatic and Hand-Feeding Blow Moulding Machine",
    category: "moulding",
    image: "prod-blow-mould",
    gallery: ["prod-blow-mould"],
    features: ["Automatic", "Semi-automatic", "Hand-feeding"],
    description:
      "Offered in automatic, semi-automatic and hand-feeding configurations, so the line matches where your operation actually is today. Start hand-fed and grow into automatic as volume justifies the investment.",
    models: [],
  },
  {
    slug: "plastic-injection-moulding-machine-80-1000-ton",
    name: "Plastic Injection Moulding Machine (80–1000 Ton)",
    category: "moulding",
    image: "prod-inject-small",
    gallery: ["prod-inject-small"],
    features: [],
    description:
      "Covers the tonnage range most general plastic injection producers need, such as caps, containers, houseware and technical parts, without stepping up to heavy industrial clamping force.",
    models: [],
  },
  {
    slug: "plastic-injection-moulding-machine-1000-2000-ton",
    name: "Plastic Injection Moulding Machine (1000–2000 Ton)",
    category: "moulding",
    image: "prod-inject-large",
    gallery: ["prod-inject-large"],
    features: [],
    description:
      "For larger, heavier mouldings that sit beyond standard injection tonnage, such as pallets, crates and large technical parts that need serious clamping force to fill and hold shape correctly.",
    models: [{ code: "NS-1300T" }],
  },
  {
    slug: "accessories-and-moulds",
    name: "Accessories and Moulds for Blow Moulding and Plastic Injection Machines",
    category: "moulding",
    image: "prod-acc-moulds",
    gallery: ["prod-acc-moulds"],
    features: ["Preform & cap moulds", "Mould temperature controllers", "Mixers, dryers & chillers"],
    description:
      "The supporting equipment that keeps a blow moulding or injection line running at consistent quality: preform and cap moulds, mould temperature controllers, mixers, dryers and chillers, all sourced alongside the machines themselves so tooling and equipment stay compatible.",
    models: [],
  },
];

const SPARE_PARTS_GROUPS = [
  { name: "Gearboxes & Reducers", image: "spare-gearbox" },
  { name: "Screw Shafts & Barrels", image: "spare-screw" },
  { name: "Control Panels & Boards", image: "spare-control" },
  { name: "Rollers, Bearings & Dies", image: "spare-roller" },
  { name: "Drive Hubs & Couplings", image: "spare-gearbox-hub" },
  { name: "Clutch & Roller Assemblies", image: "spare-clutch" },
];

function getProductBySlug(slug) {
  return PRODUCTS.find((p) => p.slug === slug);
}
function getCategoryBySlug(slug) {
  return CATEGORIES.find((c) => c.slug === slug);
}
function getProductsByCategory(slug) {
  return PRODUCTS.filter((p) => p.category === slug);
}
