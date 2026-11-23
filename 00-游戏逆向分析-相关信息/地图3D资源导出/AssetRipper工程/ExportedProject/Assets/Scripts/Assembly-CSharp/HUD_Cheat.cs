using System.Collections.Generic;
using Cheat;
using UnityEngine;

public class HUD_Cheat : Singleton<HUD_Cheat>
{
	private RectTransform mainRect;

	[SerializeField]
	private GameObject choicePrefab;

	private SimpleObjectPool pool;

	private List<HUD_CheatChoice> curChoiceList;

	public Texture[] buttonTexs;

	private ChoiceBase[] originMenu;

	private ChoiceBase[] curMenu;

	private Radio nanoRoleMenu;

	public const int Human = 1;

	public const int Nano = 2;

	public const int Terminator = 3;

	private Player myPlayer => null;

	public static int NanoRoleChoice => 0;

	protected override void Awake()
	{
	}

	public override void SetVisible(bool visible)
	{
	}

	private void RefreshAnim()
	{
	}

	private void InitChoice()
	{
	}

	private void PlayerController_FocusHUD_Listenner(ref string value)
	{
	}

	public void ResetChoice(ChoiceBase[] choices)
	{
	}

	private void UpdateInvincible(bool value)
	{
	}

	private void TryBecomeSavior()
	{
	}

	private void TryBecomeHero(NanoRole role)
	{
	}

	private void TryBecomeTerminator(NanoRole role)
	{
	}

	private void TryGiveWeapon(int wpnID)
	{
	}
}
