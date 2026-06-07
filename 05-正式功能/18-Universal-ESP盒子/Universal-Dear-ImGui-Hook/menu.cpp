#include "stdafx.h"

namespace menu {
    bool isOpen = false;

    void Init() {
        // Begin frame UI setup
        DebugLog("[menu] Rendering menu. isOpen=%d\n", isOpen);

        ImGuiIO& io = ImGui::GetIO();
        io.MouseDrawCursor = isOpen;

        if (!isOpen) {
            return;
        }

        // Style setup (one-time)
        static bool styled = false;
        if (!styled) {
            ImGui::StyleColorsDark();
            ImVec4* colors = ImGui::GetStyle().Colors;
            // Custom color palette
            colors[ImGuiCol_WindowBg] = ImVec4(0, 0, 0, 0.8f);
            colors[ImGuiCol_Header] = ImVec4(0.2f, 0.2f, 0.2f, 0.8f);
            colors[ImGuiCol_HeaderHovered] = ImVec4(0.3f, 0.3f, 0.3f, 0.8f);
            colors[ImGuiCol_Button] = ImVec4(0.26f, 0.59f, 0.98f, 0.4f);
            colors[ImGuiCol_ButtonHovered] = ImVec4(0.26f, 0.59f, 0.98f, 1.0f);
            colors[ImGuiCol_ButtonActive] = ImVec4(0.06f, 0.53f, 0.98f, 1.0f);
            styled = true;
            DebugLog("[menu] Style applied.\n");
        }

        // Window flags
        ImGuiWindowFlags flags = ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoCollapse;
        ImGui::SetNextWindowSize(ImVec2(450, 600), ImGuiCond_FirstUseEver);
        ImGui::SetNextWindowPos(ImVec2(25, 25), ImGuiCond_FirstUseEver);

        ImGui::Begin("ImGui Menu", &isOpen, flags);

        if (ImGui::CollapsingHeader("ESP SETTINGS")) {
            bool& espEnabled = esp::ESPRenderer::Enabled();
            bool prevEnabled = espEnabled;
            if (ImGui::Checkbox("Enable ESP", &espEnabled)) {
                DebugLog("[menu] ESP toggled: %d\n", espEnabled);
                // Clear cache when disabled
                if (prevEnabled && !espEnabled) {
                    esp::GameManager::OnRoomChanged();
                    DebugLog("[menu] ESP disabled, cleared bot cache\n");
                }
            }
            
            ImGui::Separator();
            ImGui::Text("ESP Status:");
            ImGui::BulletText("Initialized: %s", esp::ESPRenderer::IsInitialized() ? "Yes" : "No");
            ImGui::BulletText("IL2CPP: %s", esp::IL2CPPBridge::IsInitialized() ? "OK" : "N/A");
            ImGui::BulletText("GameManager: %s", esp::GameManager::IsInitialized() ? "OK" : "N/A");
            ImGui::BulletText("Transform: %s", esp::TransformHelper::IsInitialized() ? "OK" : "N/A");
            ImGui::BulletText("CoordConv: %s", esp::CoordConverter::IsInitialized() ? "OK" : "N/A");
            
            ImGui::Separator();
            ImGui::Text("Config:");
            ImGui::BulletText("Max Distance: %.1f", esp::config::MAX_DISTANCE);
            ImGui::BulletText("Box Thickness: %.1f", esp::config::BOX_THICKNESS);
        }

        ImGui::End();
    }
}
