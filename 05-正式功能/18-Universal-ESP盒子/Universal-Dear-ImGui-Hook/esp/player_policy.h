#pragma once

#include <cstdint>

namespace esp {
namespace policy {

constexpr int TEAM_BLACK_LIST = 0;
constexpr int TEAM_GLOBAL_RISK = 1;
constexpr int TEAM_NEUTRAL = 2;

constexpr int GameModeTeamDeath = 0;
constexpr int GameModeDeathMatch = 1;
constexpr int GameModeSpecial = 2;
constexpr int GameModeNano3 = 3;
constexpr int GameModeNano4 = 4;
constexpr int GameModeNano6 = 5;
constexpr int GameModeNano4Terminator = 6;

enum PlayerSource : std::uint32_t {
    SourceNone = 0,
    SourceAllPlayers = 1u << 0,
    SourceBL = 1u << 1,
    SourceGR = 1u << 2,
    SourceBLAlive = 1u << 3,
    SourceGRAlive = 1u << 4,
    SourceBotUpdate = 1u << 5,
};

constexpr std::uint32_t BOT_FRESH_MS = 1000u;

constexpr bool HasSource(std::uint32_t sources, PlayerSource source) {
    return (sources & static_cast<std::uint32_t>(source)) != 0u;
}

constexpr bool IsNanoMode(int gameMode) {
    return gameMode >= GameModeNano3 && gameMode <= GameModeNano4Terminator;
}

constexpr bool IsKnownGameMode(int gameMode) {
    return gameMode >= GameModeTeamDeath && gameMode <= GameModeNano4Terminator;
}

constexpr bool IsSameTeamByGameRule(int localTeam, int targetTeam) {
    if (localTeam == TEAM_NEUTRAL || targetTeam == TEAM_NEUTRAL) return false;
    return localTeam == targetTeam;
}

constexpr bool IsBotFresh(std::uint32_t lastSeen, std::uint32_t now) {
    return static_cast<std::uint32_t>(now - lastSeen) <= BOT_FRESH_MS;
}

constexpr bool IsSourceEligible(int gameMode, std::uint32_t sources, bool botFresh) {
    const bool inAlive = HasSource(sources, SourceBLAlive) ||
                         HasSource(sources, SourceGRAlive);
    const bool freshBot = HasSource(sources, SourceBotUpdate) && botFresh;
    if (gameMode == GameModeDeathMatch) {
        return HasSource(sources, SourceAllPlayers) || freshBot;
    }
    if (gameMode == GameModeTeamDeath || gameMode == GameModeSpecial) {
        return inAlive;
    }
    if (IsNanoMode(gameMode)) {
        return inAlive || freshBot;
    }
    return false;
}

} // namespace policy
} // namespace esp
