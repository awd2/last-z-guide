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

EVENT_HUB_PAGES = {
    "events.html",
}

DAILY_ROUTINE_PAGES = {
    "daily.html",
}

ALLIANCE_DUEL_PAGES = {
    "alliance-duel.html",
}

SVS_WAR_STATE_PAGES = {
    "svs.html",
}

SPEND_SAVE_EVENT_PAGES = {
    "gacha-go.html",
    "lucky-discounter.html",
}

COMBAT_RALLY_EVENT_PAGES = {
    "canyon-clash.html",
    "furylord.html",
    "tyrant.html",
    "zombie-siege.html",
}

CODE_HUB_PAGES = {
    "codes.html",
}

GIFT_CENTER_SETUP_PAGES = {
    "gift-center-uid.html",
}

CODE_TROUBLESHOOTING_PAGES = {
    "redeem-code-not-working.html",
}

POWER_GUIDE_PAGES = {
    "power-guide.html",
}

F2P_GUIDE_PAGES = {
    "f2p.html",
}

RESEARCH_GUIDE_PAGES = {
    "research.html",
}

TIPS_GUIDE_PAGES = {
    "tips.html",
}

RESOURCES_GUIDE_PAGES = {
    "resources.html",
}

HQ_GUIDE_PAGES = {
    "hq.html",
}

TECH_GUIDE_PAGES = {
    "tech.html",
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
                <li><strong>Review basis:</strong> Radar advice was checked against refresh timing, cap-loss risk, Sunday/Monday and Thursday/Friday Alliance Duel sync, and daily event routing.</li>
                <li><strong>Last checked:</strong> March 2026 for radar timing and weekly event alignment.</li>
                <li><strong>Watch for changes:</strong> task pools, refresh value, rewards, and daily-event timing can change after updates.</li>
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
                <li><strong>Last reviewed for Season 4 hero priorities and faction routing:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> faction roles, troop matching, 3rd-skill value, linked Queenie and Yu Chan profiles, formation guidance, PvP counter logic, and current hero-resource constraints.</li>
                <li><strong>Changes to watch:</strong> new-season heroes, faction prevalence, hero balance, exclusive equipment timing, and server meta can change which heroes are safest to invest in first.</li>
            </ul>
        </section>

"""

SPANISH_HERO_HUB_BLOCK = """        <section class="verification-note" aria-label="Verificación y revisión">
            <p class="verification-note-title">Verificación y revisión</p>
            <ul>
                <li><strong>Última revisión para prioridades de héroes de Temporada 4 y rutas de facción:</strong> marzo de 2026.</li>
                <li><strong>Revisado contra:</strong> roles de facción, emparejamiento de tropas, valor de la 3.ª habilidad, perfiles enlazados de Queenie y Yu Chan, formación, lógica PvP y límites de recursos de héroes.</li>
                <li><strong>Cambios a vigilar:</strong> nuevos héroes de temporada, popularidad de facciones, balance, equipo exclusivo y meta del servidor pueden cambiar qué héroes conviene potenciar primero.</li>
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
            <p>Use this tier list to choose a main faction and main five heroes, then compare it against your built roster and server meta before spending fragments, books, gear, or exclusive items.</p>
        </section>
"""

SPANISH_HERO_HUB_DISCLAIMER = """        <section class="disclaimer">
            <p>Usa esta tier list para elegir facción y cinco héroes principales, pero compárala con tu roster construido y la meta de tu servidor antes de gastar fragmentos, libros, equipo o piezas exclusivas.</p>
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

EVENT_HUB_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Event priority advice was checked against current event routing, spend/save timing, linked event guides, and site economy rules.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> event rotation, reward screens, scoring windows, and server-specific timing can change after updates.</li>
            </ul>
        </section>

"""

DAILY_ROUTINE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Daily routine advice was checked against common reset tasks, event routing, exposed-resource risk, and linked safety/economy guides.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> daily reset timing, event tasks, shop stock, and server risk windows can change after updates.</li>
            </ul>
        </section>

"""

ALLIANCE_DUEL_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Alliance Duel advice was checked against day-by-day scoring, saved-item timing, Duel Shop value, and linked reward/research pages.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> scoring tasks, reward thresholds, shop stock, and server event timing can change after updates.</li>
            </ul>
        </section>

"""

SVS_WAR_STATE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> SVS advice was checked against war-state timing, invasion/defense roles, shield discipline, PvP risk, and linked event/economy guidance.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> war rules, state matchmaking, shield timing, scoring windows, and troop-loss risk can change after updates or by server group.</li>
            </ul>
        </section>

"""

SPEND_SAVE_EVENT_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Spend-event advice was checked against current reward logic, saved-currency timing, site economy rules, and linked F2P/value guides.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> reward pools, discount values, milestone thresholds, and event timing can change after updates.</li>
            </ul>
        </section>

"""

COMBAT_RALLY_EVENT_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Review basis:</strong> Combat-event advice was checked against current event flow, scoring logic, rally/formation requirements, reward timing, and linked PvP/event guides.</li>
                <li><strong>Last reviewed for the current patch and season context:</strong> March 2026.</li>
                <li><strong>Use caution:</strong> event rules, damage scaling, reward tiers, formation value, and alliance timing can change after updates.</li>
            </ul>
        </section>

"""

EVENT_HUB_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page to choose which event guide to open next, then verify the live event timer and reward screen before spending saved items.</p>
        </section>
"""

DAILY_ROUTINE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as a daily checklist, then confirm live timers, exposed resources, and shield needs before logging off or spending saved items.</p>
        </section>
"""

ALLIANCE_DUEL_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this to plan your week, then verify the live Alliance Duel day, scoring task, and reward screen before spending speed-ups, badges, or saved items.</p>
        </section>
"""

SVS_WAR_STATE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as SVS planning support, then check live state rules, timers, shield coverage, and alliance calls before teleporting or attacking.</p>
        </section>
"""

SPEND_SAVE_EVENT_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this to decide whether the event is worth your saved currency, then confirm the live reward pool and milestone values before spending diamonds or tickets.</p>
        </section>
"""

COMBAT_RALLY_EVENT_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as event execution guidance, then verify the live event rules, reward tiers, and alliance timing before committing troops, stamina, or saved combat items.</p>
        </section>
"""

CODE_HUB_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for code availability and Gift Center flow:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> official Gift Center redemption behavior, UID requirements, mailbox reward delivery, and the linked setup and troubleshooting guides.</li>
                <li><strong>Changes to watch:</strong> code expiry, already-used status, campaign availability, reward contents, and temporary Gift Center outages can change faster than normal guide mechanics.</li>
            </ul>
        </section>

"""

GIFT_CENTER_SETUP_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for UID setup and Gift Center login flow:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> the official Gift Center flow, the in-game UID path (Avatar -> Settings -> Copy ID), mobile browser redemption, mailbox delivery, and the related codes and troubleshooting pages.</li>
                <li><strong>Changes to watch:</strong> Gift Center page availability, login labels, UID copy path, browser behavior, and mailbox timing may shift after game or web updates.</li>
            </ul>
        </section>

"""

CODE_TROUBLESHOOTING_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for code troubleshooting and Gift Center errors:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> common failed-redemption causes, wrong UID entry, expired or already-used codes, official Gift Center behavior, mailbox delays, and the linked setup and codes pages.</li>
                <li><strong>Changes to watch:</strong> error wording, code status, account or server eligibility, reward delays, and temporary Gift Center outages can change without notice.</li>
            </ul>
        </section>

"""

CODE_HUB_DISCLAIMER = """        <section class="disclaimer">
            <p>This page is for finding current Last Z codes and redeeming them through the official Gift Center. Always paste your UID directly from the game, check the live Gift Center response, and confirm rewards in your in-game mailbox.</p>
        </section>
"""

GIFT_CENTER_SETUP_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this setup guide before redeeming Last Z codes. Copy your UID from the game instead of typing it manually, redeem through the official Gift Center, and check your mailbox after a successful submission.</p>
        </section>
"""

CODE_TROUBLESHOOTING_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this checklist before retrying a failed Last Z code. Verify the official Gift Center is loading, copy your UID directly from the game, match the code text exactly, and allow for mailbox delay after a successful redemption.</p>
        </section>
"""

POWER_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for power-growth routing:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> HQ requirements, research power, troop training, hero investment, vehicle upgrades, shop priorities, and related progression/economy guides.</li>
                <li><strong>Changes to watch:</strong> displayed power formulas, event rewards, shop stock, vehicle materials, VIP value, and research unlocks can change after updates.</li>
            </ul>
        </section>

"""

F2P_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for F2P diamond and shop priorities:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> reserve-first diamond rules, shield safety, refugee value, free diamond sources, shop priority, event timing, and low-spender/F2P constraints.</li>
                <li><strong>Changes to watch:</strong> shop stock, event milestones, shield pricing, refugee value, diamond sources, and server pressure can change after updates.</li>
            </ul>
        </section>

"""

RESEARCH_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for research order and T10 planning:</strong> May 2026.</li>
                <li><strong>Checked against:</strong> the canonical route from Hero Training to Cockpit, Military Strategies, Peace Shield/Urgent Rescue, the optional Siege to Seize -> Field Research route, linked branch cost pages, and UST/T10 planning context.</li>
                <li><strong>Changes to watch:</strong> badge costs, branch prerequisites, node names, unlock requirements, and late-game research value can change after research updates.</li>
            </ul>
        </section>

"""

TIPS_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for practical strategy coverage:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> HQ priority, alliance value, focused hero development, daily activity routing, saved-resource timing, and linked progression/economy guides.</li>
                <li><strong>Changes to watch:</strong> event tasks, alliance rewards, building requirements, hero meta, and resource bottlenecks can change after updates or by server age.</li>
            </ul>
        </section>

"""

RESOURCES_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for resource farming and protection:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> gathering value, steel sources, chest timing, diamond reserve rules, warehouse protection, farm-account use cases, and related economy guides.</li>
                <li><strong>Changes to watch:</strong> gathering rewards, chest payouts, steel sources, raid pressure, resource building output, and farm-account rules can change after updates.</li>
            </ul>
        </section>

"""

HQ_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for HQ path and construction requirements:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> HQ level gates, required-building patterns, Sophia construction value, steel phase planning, Alliance Duel timing, and related progression/resource guides.</li>
                <li><strong>Changes to watch:</strong> required buildings, steel availability, construction bonuses, HQ skin values, T11 timing, and server-stage unlocks can change after updates.</li>
            </ul>
        </section>

"""

TECH_GUIDE_BLOCK = """        <section class="verification-note" aria-label="Verification and review">
            <p class="verification-note-title">Verification &amp; Review</p>
            <ul>
                <li><strong>Last reviewed for F2P and low-spender tech routing:</strong> March 2026.</li>
                <li><strong>Checked against:</strong> Alliance Recognition tradeoffs, Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, HP stacking, HQ27 trap context, and linked research cost pages.</li>
                <li><strong>Changes to watch:</strong> branch prerequisites, badge costs, unlock names, Fully Armed Alliance value, HP stacking effects, and server meta can change after updates.</li>
            </ul>
        </section>

"""

POWER_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page to choose the next useful power source, not to chase empty CP. Confirm live costs before spending speedups, badges, diamonds, vehicle parts, or hero materials.</p>
        </section>
"""

F2P_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this as a F2P spending filter before buying. Keep emergency diamonds protected first, then compare the live shop or event screen before spending saved currency.</p>
        </section>
"""

RESEARCH_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page for research direction, then verify exact badge costs and unlock requirements on the linked branch pages and in-game before committing rare badges.</p>
        </section>
"""

TIPS_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use these tips as a decision checklist, then adapt them to your server age, alliance quality, current event calendar, and strongest built heroes.</p>
        </section>
"""

RESOURCES_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page to plan resource flow, then confirm live event timing, warehouse safety, and current steel or diamond sources before opening saved chests or exposing resources.</p>
        </section>
"""

HQ_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page to plan HQ pushes, then check the live requirement screen before spending construction speedups, steel, diamonds, or saved resource boxes.</p>
        </section>
"""

TECH_GUIDE_DISCLAIMER = """        <section class="disclaimer">
            <p>Use this page to choose a tech route for your account type, then confirm branch costs in-game before spending badges or delaying core combat research.</p>
        </section>
"""


def verification_block_for(page_name: str) -> str:
    if page_name in POWER_GUIDE_PAGES:
        return POWER_GUIDE_BLOCK
    if page_name in F2P_GUIDE_PAGES:
        return F2P_GUIDE_BLOCK
    if page_name in RESEARCH_GUIDE_PAGES:
        return RESEARCH_GUIDE_BLOCK
    if page_name in TIPS_GUIDE_PAGES:
        return TIPS_GUIDE_BLOCK
    if page_name in RESOURCES_GUIDE_PAGES:
        return RESOURCES_GUIDE_BLOCK
    if page_name in HQ_GUIDE_PAGES:
        return HQ_GUIDE_BLOCK
    if page_name in TECH_GUIDE_PAGES:
        return TECH_GUIDE_BLOCK
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
    if page_name in EVENT_HUB_PAGES:
        return EVENT_HUB_BLOCK
    if page_name in DAILY_ROUTINE_PAGES:
        return DAILY_ROUTINE_BLOCK
    if page_name in ALLIANCE_DUEL_PAGES:
        return ALLIANCE_DUEL_BLOCK
    if page_name in SVS_WAR_STATE_PAGES:
        return SVS_WAR_STATE_BLOCK
    if page_name in SPEND_SAVE_EVENT_PAGES:
        return SPEND_SAVE_EVENT_BLOCK
    if page_name in COMBAT_RALLY_EVENT_PAGES:
        return COMBAT_RALLY_EVENT_BLOCK
    if page_name in CODE_HUB_PAGES:
        return CODE_HUB_BLOCK
    if page_name in GIFT_CENTER_SETUP_PAGES:
        return GIFT_CENTER_SETUP_BLOCK
    if page_name in CODE_TROUBLESHOOTING_PAGES:
        return CODE_TROUBLESHOOTING_BLOCK
    return FULL_BLOCK


def disclaimer_for(page_name: str) -> str | None:
    if page_name in POWER_GUIDE_PAGES:
        return POWER_GUIDE_DISCLAIMER
    if page_name in F2P_GUIDE_PAGES:
        return F2P_GUIDE_DISCLAIMER
    if page_name in RESEARCH_GUIDE_PAGES:
        return RESEARCH_GUIDE_DISCLAIMER
    if page_name in TIPS_GUIDE_PAGES:
        return TIPS_GUIDE_DISCLAIMER
    if page_name in RESOURCES_GUIDE_PAGES:
        return RESOURCES_GUIDE_DISCLAIMER
    if page_name in HQ_GUIDE_PAGES:
        return HQ_GUIDE_DISCLAIMER
    if page_name in TECH_GUIDE_PAGES:
        return TECH_GUIDE_DISCLAIMER
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
    if page_name in EVENT_HUB_PAGES:
        return EVENT_HUB_DISCLAIMER
    if page_name in DAILY_ROUTINE_PAGES:
        return DAILY_ROUTINE_DISCLAIMER
    if page_name in ALLIANCE_DUEL_PAGES:
        return ALLIANCE_DUEL_DISCLAIMER
    if page_name in SVS_WAR_STATE_PAGES:
        return SVS_WAR_STATE_DISCLAIMER
    if page_name in SPEND_SAVE_EVENT_PAGES:
        return SPEND_SAVE_EVENT_DISCLAIMER
    if page_name in COMBAT_RALLY_EVENT_PAGES:
        return COMBAT_RALLY_EVENT_DISCLAIMER
    if page_name in CODE_HUB_PAGES:
        return CODE_HUB_DISCLAIMER
    if page_name in GIFT_CENTER_SETUP_PAGES:
        return GIFT_CENTER_SETUP_DISCLAIMER
    if page_name in CODE_TROUBLESHOOTING_PAGES:
        return CODE_TROUBLESHOOTING_DISCLAIMER
    return None


def sync_page(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    block = verification_block_for(path.name)
    disclaimer = disclaimer_for(path.name)

    verification_pattern = re.compile(
        r'\s*(?:<section class="verification-note"[^>]*>.*?</section>\s*)+',
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
