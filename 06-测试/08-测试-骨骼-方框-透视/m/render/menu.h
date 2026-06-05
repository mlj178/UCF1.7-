#pragma once

class Menu {
public:
    static Menu& Instance();
    
    void Render();
    void Toggle() { m_Open = !m_Open; }
    bool IsOpen() const { return m_Open; }
    
private:
    Menu() = default;
    ~Menu() = default;
    
    bool m_Open = false;
    
    void RenderMainWindow();
    void RenderSettingsWindow();
};
