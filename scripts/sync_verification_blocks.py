#!/usr/bin/env python3
"""Insert or refresh verification blocks across content pages."""

from __future__ import annotations

import re
from pathlib import Path

from site_utils import ROOT, list_html_pages


EXCLUDED = {
    "index.html",
    "about.html",
    "contact.html",
    "privacy.html",
    "terms.html",
    "disclosure.html",
    "news-preview.html",
}

RESEARCH_BRANCH_PAGES = {
    "army-building-cost.html",
    "field-research.html",
    "fully-armed-alliance-cost.html",
    "hero-training-cost.html",
    "military-strategies-cost.html",
    "peace-shield-cost.html",
    "siege-to-seize-cost.html",
    "unit-special-training-cost.html",
}

STATIC_DATA_PAGES = {
    "alliance-duel-rewards.html",
    "alliance-recognition-cost.html",
    "emergency-hospital-cost.html",
    "hq-construction-cost.html",
    "vehicle-modification-cost.html",
}

PROGRESSION_PLANNING_PAGES = {
    "base-building-order.html",
    "early-game-optimization.html",
    "hq.html",
    "leveling.html",
    "power-guide.html",
    "shooter-stages.html",
    "start.html",
}

ECONOMY_RESERVE_PAGES = {
    "diamond-reserve.html",
    "f2p.html",
    "refugees.html",
    "resources.html",
    "steel.html",
}

FARM_ACCOUNT_PAGES = {
    "farm-account.html",
}

SHIELD_SAFETY_PAGES = {
    "shield.html",
}

DAILY_UTILITY_PAGES = {
    "radar.html",
}

ARENA_SUPPORT_PAGES = {
    "arena.html",
}

RESEARCH_SYSTEM_PAGES = {
    "tech.html",
}

HERO_HUB_PAGES = {
    "heroes.html",
}

SPANISH_HERO_HUB_PAGES = {
    "heroes-es.html",
}

HERO_PROFILE_PAGES = {
    "queenie.html",
    "yu-chan.html",
}

FORMATION_STRATEGY_PAGES = {
    "formations.html",
}

FORMATION_POWER_PAGES = {
    "formation-power.html",
}

PVP_TRAP_PAGES = {
    "pvp.html",
    "trap.html",
}

EQUIPMENT_GEAR_PAGES = {
    "gear.html",
}

FULL_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>How this guide was verified:</strong> Based on in-game data, tested results, and cross-checks against community validation.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Source pattern:</strong> In-game data + tested results + community validation.</li>
            </ul>
        </section>

"""

RESEARCH_BRANCH_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Branch totals were checked against the generated research data source, in-game value checks, and cumulative badge calculations.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> badge costs, unlock requirements, node names, and branch prerequisites can change after research updates.</li>
            </ul>
        </section>

"""

STATIC_DATA_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Tables and totals were checked against in-game values, visible requirements, and practical planning use cases.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> costs, rewards, shop values, and event thresholds can change after updates or by server group.</li>
            </ul>
        </section>

"""

RESEARCH_BRANCH_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page as planning data before spending badges or saved resources, and confirm final values in-game before committing rare materials.</p>
        </section>
"""

STATIC_DATA_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page for planning, then confirm the current in-game value before spending badges, diamonds, speedups, or rare event items.</p>
        </section>
"""

PROGRESSION_PLANNING_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Progression advice was checked against current in-game systems, HQ and resource bottlenecks, unlock flow, and practical account-stage tradeoffs.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> upgrade requirements, event rewards, shop stock, and server timing can change after updates.</li>
            </ul>
        </section>

"""

ECONOMY_RESERVE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Economy advice was checked against site canonical reserve-first rules, resource bottlenecks, event-value tradeoffs, and F2P account constraints.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> shop stock, event rewards, resource packages, and server pressure can change after updates.</li>
            </ul>
        </section>

"""

FARM_ACCOUNT_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Farm-account guidance was checked against practical resource-transfer use cases, account safety concerns, and current site economy rules.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> account rules, transfer limits, event behavior, and server enforcement can change after updates.</li>
            </ul>
        </section>

"""

SHIELD_SAFETY_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Shield guidance was checked against reserve-first diamond rules, Alliance Shop shield value, PvP risk windows, and saved-resource protection.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> Alliance Shop stock, shield pricing, server war timing, and event pressure can change after updates.</li>
            </ul>
        </section>

"""

DAILY_UTILITY_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Radar advice was checked against the current Radar workflow, task priority logic, refresh value, and daily event routing.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> task pools, refresh value, rewards, and daily-event timing can change after updates.</li>
            </ul>
        </section>

"""

ARENA_SUPPORT_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Arena advice was checked against daily attempt flow, reward timing, formation matchup logic, and related PvP guidance.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> matchmaking, rewards, formation meta, and server competition can change after updates.</li>
            </ul>
        </section>

"""

RESEARCH_SYSTEM_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Research and tech-priority advice was checked against the site's mainline research route, unlock checkpoints, and linked branch cost pages.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> branch prerequisites, badge costs, unlock names, and late-game tech value can change after research updates.</li>
            </ul>
        </section>

"""

PROGRESSION_PLANNING_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as decision support, then confirm current in-game values before spending diamonds, speedups, badges, or saved resources.</p>
        </section>
"""

ECONOMY_RESERVE_DISCLAIMER = """        <section class="disclaimer">
            <p>Protect reserve resources first, then confirm current shop and event values before spending diamonds or saved items.</p>
        </section>
"""

FARM_ACCOUNT_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as a risk-aware planning guide, and check current game/account rules before building a long-term farm setup.</p>
        </section>
"""

SHIELD_SAFETY_DISCLAIMER = """        <section class="disclaimer">
            <p>Check Alliance Shop stock and current server risk before spending diamonds on shields directly.</p>
        </section>
"""

DAILY_UTILITY_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this to choose Radar tasks faster, then confirm the live task reward before spending refreshes or saved resources.</p>
        </section>
"""

ARENA_SUPPORT_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as a daily Arena checklist, then compare matchups against your server meta before spending extra attempts or formation resources.</p>
        </section>
"""

RESEARCH_SYSTEM_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this to choose research direction, then confirm exact branch requirements on the linked cost pages and in-game before spending badges.</p>
        </section>
"""

HERO_HUB_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Hero priorities were checked against current faction roles, troop matching, linked hero profiles, formation guidance, and PvP matchup logic.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> hero balance, server meta, faction prevalence, and new-season heroes can change after updates.</li>
            </ul>
        </section>

"""

SPANISH_HERO_HUB_BLOCK = """        <section class="verification-note" aria-label="Verificación y revisión">
            <p class="verification-note-title">Verificación y revisión</p>
            <ul>
                <li><strong>Base de revisión:</strong> Las prioridades de héroes se revisaron contra roles de facción, emparejamiento de tropas, guías de formación/PvP enlazadas y recomendaciones canónicas del sitio.</li>
                <li><strong>Última revisión para el parche y contexto de temporada actuales:</strong> marzo de 2026.</li>
                <li><strong>Ten cuidado:</strong> el balance de héroes, la meta del servidor, la popularidad de facciones y los héroes de nuevas temporadas pueden cambiar con actualizaciones.</li>
            </ul>
        </section>

"""

HERO_PROFILE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Hero build advice was checked against visible skill text, faction role, troop alignment, exclusive talent effects, and linked formation guidance.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> skill values, talent effects, hero balance, and faction meta can change after updates.</li>
            </ul>
        </section>

"""

FORMATION_STRATEGY_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Formation advice was checked against faction counters, 3+2 matchup logic, troop alignment, hero role coverage, and related PvP guidance.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> server faction mix, available heroes, new-season releases, and PvP meta can change after updates.</li>
            </ul>
        </section>

"""

FORMATION_POWER_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Formation power guidance was checked against displayed power levers, same-faction bonuses, troop-capacity sources, research effects, and related formation/PvP pages.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> power formulas, faction bonuses, research effects, and Hall of Honor values can change after updates.</li>
            </ul>
        </section>

"""

PVP_TRAP_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> PvP guidance was checked against scouting signals, faction-counter logic, formation matchup rules, shield discipline, and related SVS/trap guidance.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> server meta, shield timing, war rules, matchmaking, and troop-loss risk can change after updates or by server group.</li>
            </ul>
        </section>

"""

EQUIPMENT_GEAR_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Gear advice was checked against equipment tiers, enhancement caps, promotion stages, Power Core use, mythic requirements, and main-formation priority.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> gear costs, paid material availability, enhancement caps, and event/shop sources can change after updates.</li>
            </ul>
        </section>

"""

HERO_HUB_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as a prioritization guide, then compare it against your built roster and server meta before spending fragments, books, gear, or exclusive items.</p>
        </section>
"""

SPANISH_HERO_HUB_DISCLAIMER = """        <section class="disclaimer">
            <p>Usa esta guía para priorizar héroes, pero compara la recomendación con tu formación ya construida y la meta de tu servidor antes de gastar fragmentos, libros o equipo.</p>
        </section>
"""

HERO_PROFILE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as hero-build guidance, then confirm the current skill text and star/talent values in-game before committing rare hero resources.</p>
        </section>
"""

FORMATION_STRATEGY_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this to choose formation logic, then test it against your server matchups and your strongest built heroes before changing faction investment.</p>
        </section>
"""

FORMATION_POWER_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this to understand displayed formation power, but do not treat the power number as the only PvP goal; test matchups against your server meta.</p>
        </section>
"""

PVP_TRAP_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as PvP decision support, then scout, check live server conditions, and protect critical resources before attacking or setting a trap.</p>
        </section>
"""

EQUIPMENT_GEAR_DISCLAIMER = """        <section class="disclaimer">
            <p>Confirm current gear costs and upgrade caps in-game before spending Power Cores, alloys, mythic materials, or saved equipment resources.</p>
        </section>
"""


def verification_block_for(page_name: str) -> str:
    if page_name in RESEARCH_BRANCH_PAGES:
        return RESEARCH_BRANCH_BLOCK
    if page_name in STATIC_DATA_PAGES:
        return STATIC_DATA_BLOCK
    if page_name in PROGRESSION_PLANNING_PAGES:
        return PROGRESSION_PLANNING_BLOCK
    if page_name in ECONOMY_RESERVE_PAGES:
        return ECONOMY_RESERVE_BLOCK
    if page_name in FARM_ACCOUNT_PAGES:
        return FARM_ACCOUNT_BLOCK
    if page_name in SHIELD_SAFETY_PAGES:
        return SHIELD_SAFETY_BLOCK
    if page_name in DAILY_UTILITY_PAGES:
        return DAILY_UTILITY_BLOCK
    if page_name in ARENA_SUPPORT_PAGES:
        return ARENA_SUPPORT_BLOCK
    if page_name in RESEARCH_SYSTEM_PAGES:
        return RESEARCH_SYSTEM_BLOCK
    if page_name in HERO_HUB_PAGES:
        return HERO_HUB_BLOCK
    if page_name in SPANISH_HERO_HUB_PAGES:
        return SPANISH_HERO_HUB_BLOCK
    if page_name in HERO_PROFILE_PAGES:
        return HERO_PROFILE_BLOCK
    if page_name in FORMATION_STRATEGY_PAGES:
        return FORMATION_STRATEGY_BLOCK
    if page_name in FORMATION_POWER_PAGES:
        return FORMATION_POWER_BLOCK
    if page_name in PVP_TRAP_PAGES:
        return PVP_TRAP_BLOCK
    if page_name in EQUIPMENT_GEAR_PAGES:
        return EQUIPMENT_GEAR_BLOCK
    return FULL_BLOCK


def disclaimer_for(page_name: str) -> str | None:
    if page_name in RESEARCH_BRANCH_PAGES:
        return RESEARCH_BRANCH_DISCLAIMER
    if page_name in STATIC_DATA_PAGES:
        return STATIC_DATA_DISCLAIMER
    if page_name in PROGRESSION_PLANNING_PAGES:
        return PROGRESSION_PLANNING_DISCLAIMER
    if page_name in ECONOMY_RESERVE_PAGES:
        return ECONOMY_RESERVE_DISCLAIMER
    if page_name in FARM_ACCOUNT_PAGES:
        return FARM_ACCOUNT_DISCLAIMER
    if page_name in SHIELD_SAFETY_PAGES:
        return SHIELD_SAFETY_DISCLAIMER
    if page_name in DAILY_UTILITY_PAGES:
        return DAILY_UTILITY_DISCLAIMER
    if page_name in ARENA_SUPPORT_PAGES:
        return ARENA_SUPPORT_DISCLAIMER
    if page_name in RESEARCH_SYSTEM_PAGES:
        return RESEARCH_SYSTEM_DISCLAIMER
    if page_name in HERO_HUB_PAGES:
        return HERO_HUB_DISCLAIMER
    if page_name in SPANISH_HERO_HUB_PAGES:
        return SPANISH_HERO_HUB_DISCLAIMER
    if page_name in HERO_PROFILE_PAGES:
        return HERO_PROFILE_DISCLAIMER
    if page_name in FORMATION_STRATEGY_PAGES:
        return FORMATION_STRATEGY_DISCLAIMER
    if page_name in FORMATION_POWER_PAGES:
        return FORMATION_POWER_DISCLAIMER
    if page_name in PVP_TRAP_PAGES:
        return PVP_TRAP_DISCLAIMER
    if page_name in EQUIPMENT_GEAR_PAGES:
        return EQUIPMENT_GEAR_DISCLAIMER
    return None


def sync_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    block = verification_block_for(path.name)
    disclaimer = disclaimer_for(path.name)

    verification_pattern = re.compile(
        r'\s*<section class="verification-note" aria-label="Verification and review">.*?</section>\s*',
        re.S,
    )
    disclaimer_pattern = re.compile(r'(<section class="disclaimer">)', re.S)
    full_disclaimer_pattern = re.compile(
        r'\s*<section class="disclaimer">.*?</section>',
        re.S,
    )

    if verification_pattern.search(text):
        text = verification_pattern.sub("\n" + block, text, count=1)
    elif disclaimer_pattern.search(text):
        text = disclaimer_pattern.sub("\n" + block + r"\1", text, count=1)

    if disclaimer and full_disclaimer_pattern.search(text):
        text = full_disclaimer_pattern.sub("\n" + disclaimer, text, count=1)
        text = re.sub(
            r'\n{2,}\s*<section class="related-guides">',
            '\n\n        <section class="related-guides">',
            text,
            count=1,
        )
        text = re.sub(
            r'\n{2,}\s*<!-- Related Guides -->\s*<section class="related-guides">',
            '\n\n        <!-- Related Guides -->\n        <section class="related-guides">',
            text,
            count=1,
        )
    else:
        text = re.sub(
            r'(This guide was last validated in )([A-Za-z]+ \d{4})(\.)',
            r"\1March 2026\3",
            text,
        )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    updated = 0
    for path in list_html_pages():
        if path.name in EXCLUDED:
            continue
        if sync_page(path):
            updated += 1
    print(f"Updated verification blocks on {updated} HTML files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
