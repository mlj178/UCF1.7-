#include "config.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

ESPConfig g_Config;

bool ESPConfig::LoadFromFile(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) {
        return false;
    }
    
    char line[256];
    char section[64] = "";
    
    while (fgets(line, sizeof(line), f)) {
        char* p = line;
        while (*p == ' ' || *p == '\t') p++;
        
        if (*p == '[') {
            char* end = strchr(p, ']');
            if (end) {
                *end = '\0';
                strncpy(section, p + 1, sizeof(section) - 1);
            }
            continue;
        }
        
        if (*p == ';' || *p == '#' || *p == '\n') {
            continue;
        }
        
        char* eq = strchr(p, '=');
        if (!eq) continue;
        
        *eq = '\0';
        char* key = p;
        char* value = eq + 1;
        
        while (*key == ' ' || *key == '\t') key++;
        char* keyEnd = key + strlen(key) - 1;
        while (keyEnd > key && (*keyEnd == ' ' || *keyEnd == '\t')) *keyEnd-- = '\0';
        
        while (*value == ' ' || *value == '\t') value++;
        char* valueEnd = value + strlen(value) - 1;
        while (valueEnd > value && (*valueEnd == ' ' || *valueEnd == '\t' || *valueEnd == '\n')) *valueEnd-- = '\0';
        
        if (strcmp(section, "ESP") == 0) {
            if (strcmp(key, "Enabled") == 0) enabled = atoi(value) != 0;
            else if (strcmp(key, "ShowBox") == 0) showBox = atoi(value) != 0;
            else if (strcmp(key, "ShowSkeleton") == 0) showSkeleton = atoi(value) != 0;
            else if (strcmp(key, "ShowDistance") == 0) showDistance = atoi(value) != 0;
            else if (strcmp(key, "ShowHealth") == 0) showHealth = atoi(value) != 0;
        }
        else if (strcmp(section, "Hotkeys") == 0) {
            if (strcmp(key, "OpenMenu") == 0) openMenuKey = atoi(value);
            else if (strcmp(key, "Uninject") == 0) uninjectKey = atoi(value);
            else if (strcmp(key, "ToggleESP") == 0) toggleESPKey = atoi(value);
        }
        else if (strcmp(section, "Colors") == 0) {
            if (strcmp(key, "EnemyR") == 0) enemyColor.x = (float)atof(value);
            else if (strcmp(key, "EnemyG") == 0) enemyColor.y = (float)atof(value);
            else if (strcmp(key, "EnemyB") == 0) enemyColor.z = (float)atof(value);
            else if (strcmp(key, "EnemyA") == 0) enemyColor.w = (float)atof(value);
            else if (strcmp(key, "TeamR") == 0) teamColor.x = (float)atof(value);
            else if (strcmp(key, "TeamG") == 0) teamColor.y = (float)atof(value);
            else if (strcmp(key, "TeamB") == 0) teamColor.z = (float)atof(value);
            else if (strcmp(key, "TeamA") == 0) teamColor.w = (float)atof(value);
        }
        else if (strcmp(section, "Render") == 0) {
            if (strcmp(key, "BoxThickness") == 0) boxThickness = (float)atof(value);
            else if (strcmp(key, "SkeletonThickness") == 0) skeletonThickness = (float)atof(value);
            else if (strcmp(key, "MaxDistance") == 0) maxDistance = (float)atof(value);
        }
    }
    
    fclose(f);
    return true;
}

bool ESPConfig::SaveToFile(const char* path) {
    FILE* f = fopen(path, "w");
    if (!f) {
        return false;
    }
    
    fprintf(f, "[ESP]\n");
    fprintf(f, "Enabled=%d\n", enabled ? 1 : 0);
    fprintf(f, "ShowBox=%d\n", showBox ? 1 : 0);
    fprintf(f, "ShowSkeleton=%d\n", showSkeleton ? 1 : 0);
    fprintf(f, "ShowDistance=%d\n", showDistance ? 1 : 0);
    fprintf(f, "ShowHealth=%d\n", showHealth ? 1 : 0);
    fprintf(f, "\n");
    
    fprintf(f, "[Hotkeys]\n");
    fprintf(f, "OpenMenu=%d\n", openMenuKey);
    fprintf(f, "Uninject=%d\n", uninjectKey);
    fprintf(f, "ToggleESP=%d\n", toggleESPKey);
    fprintf(f, "\n");
    
    fprintf(f, "[Colors]\n");
    fprintf(f, "EnemyR=%.2f\n", enemyColor.x);
    fprintf(f, "EnemyG=%.2f\n", enemyColor.y);
    fprintf(f, "EnemyB=%.2f\n", enemyColor.z);
    fprintf(f, "EnemyA=%.2f\n", enemyColor.w);
    fprintf(f, "TeamR=%.2f\n", teamColor.x);
    fprintf(f, "TeamG=%.2f\n", teamColor.y);
    fprintf(f, "TeamB=%.2f\n", teamColor.z);
    fprintf(f, "TeamA=%.2f\n", teamColor.w);
    fprintf(f, "\n");
    
    fprintf(f, "[Render]\n");
    fprintf(f, "BoxThickness=%.2f\n", boxThickness);
    fprintf(f, "SkeletonThickness=%.2f\n", skeletonThickness);
    fprintf(f, "MaxDistance=%.2f\n", maxDistance);
    
    fclose(f);
    return true;
}
