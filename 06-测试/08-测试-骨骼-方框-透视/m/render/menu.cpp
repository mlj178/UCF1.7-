#include "menu.h"
#include "../core/config.h"
#include "../imgui/imgui.h"

Menu& Menu::Instance() {
    static Menu instance;
    return instance;
}

void Menu::Render() {
    ImGui::Begin("ESP Menu", &m_Open, ImGuiWindowFlags_AlwaysAutoResize);
    
    ImGui::Checkbox("Enabled", &g_Config.enabled);
    ImGui::Checkbox("Show Box", &g_Config.showBox);
    ImGui::Checkbox("Show Skeleton", &g_Config.showSkeleton);
    ImGui::Checkbox("Show Distance", &g_Config.showDistance);
    ImGui::Checkbox("Show Health", &g_Config.showHealth);
    
    ImGui::Separator();
    ImGui::SliderFloat("Box Thickness", &g_Config.boxThickness, 0.5f, 5.0f);
    ImGui::SliderFloat("Skeleton Thickness", &g_Config.skeletonThickness, 0.5f, 5.0f);
    ImGui::SliderFloat("Max Distance", &g_Config.maxDistance, 100.0f, 1000.0f);
    
    ImGui::Separator();
    if (ImGui::Button("Save Config")) {
        g_Config.SaveToFile("esp_config.ini");
    }
    ImGui::SameLine();
    if (ImGui::Button("Load Config")) {
        g_Config.LoadFromFile("esp_config.ini");
    }
    
    ImGui::End();
}

void Menu::RenderMainWindow() {
    // TODO: Implement main window
}

void Menu::RenderSettingsWindow() {
    // TODO: Implement settings window
}
