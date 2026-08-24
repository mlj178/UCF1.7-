#include "../esp/player_policy.h"
#include <cassert>

using namespace esp::policy;

int main() {
    assert(!IsSameTeamByGameRule(TEAM_BLACK_LIST, TEAM_GLOBAL_RISK));
    assert(IsSameTeamByGameRule(TEAM_BLACK_LIST, TEAM_BLACK_LIST));
    assert(IsSameTeamByGameRule(TEAM_GLOBAL_RISK, TEAM_GLOBAL_RISK));
    assert(!IsSameTeamByGameRule(TEAM_NEUTRAL, TEAM_NEUTRAL));
    assert(!IsSameTeamByGameRule(TEAM_NEUTRAL, TEAM_BLACK_LIST));
    assert(!IsSameTeamByGameRule(TEAM_GLOBAL_RISK, TEAM_NEUTRAL));

    const auto all = SourceAllPlayers;
    const auto aliveBL = SourceBLAlive;
    const auto aliveGR = SourceGRAlive;
    const auto bot = SourceBotUpdate;

    assert(IsSourceEligible(GameModeDeathMatch, all, false));
    assert(IsSourceEligible(GameModeDeathMatch, bot, true));
    assert(!IsSourceEligible(GameModeDeathMatch, bot, false));

    assert(IsSourceEligible(GameModeTeamDeath, aliveBL, false));
    assert(IsSourceEligible(GameModeTeamDeath, aliveGR, false));
    assert(!IsSourceEligible(GameModeTeamDeath, all, false));
    assert(!IsSourceEligible(GameModeTeamDeath, bot, true));

    assert(IsSourceEligible(GameModeSpecial, aliveBL, false));
    assert(!IsSourceEligible(GameModeSpecial, all, false));

    assert(IsSourceEligible(GameModeNano4, aliveGR, false));
    assert(IsSourceEligible(GameModeNano4, bot, true));
    assert(!IsSourceEligible(GameModeNano4, bot, false));
    assert(!IsSourceEligible(99, all | aliveBL | bot, true));

    assert(IsBotFresh(1000u, 1500u));
    assert(IsBotFresh(0xFFFFFF00u, 0x00000050u));
    assert(!IsBotFresh(1000u, 2001u));
    return 0;
}
