using UnityEngine;

public class HUD_EscMenu : Singleton<HUD_EscMenu>
{
	[SerializeField]
	private GameObject exitMsgWnd;

	protected override void Awake()
	{
	}

	private void Update()
	{
	}

	private void PlayerController_FocusHUD_Listenner(ref string hud)
	{
	}

	public void OnCloseMenuBtnDown()
	{
	}

	public void OnGameEndBtnDown()
	{
	}

	public void SureGameEnd()
	{
	}

	public void CancelGameEnd()
	{
	}
}
