using System.Collections.Generic;
using UnityEngine;

public class HUD_KillMsg : Singleton<HUD_KillMsg>
{
	public List<HUD_KillMsgIndividual> spareMsg;

	private List<HUD_KillMsgIndividual> busyMsg;

	private Queue<float> refreshTime;

	public Sprite[] headshotIcon;

	public Sprite[] wallThroughIcon;

	public Sprite[] mulltiKillIcon;

	public Sprite[] firstAndLastKillIcon;

	[SerializeField]
	private Sprite nanoKillHeroIcon;

	[SerializeField]
	private Sprite nanoMeleeDeathIcon;

	public Material additiveMaterial;

	public static Color vvipFlashColor;

	private static readonly Color color_BL;

	private static readonly Color color_GR;

	private static readonly Color color_NanoGhost;

	private static readonly Color color_Human;

	private static readonly Color color_DM_Me;

	private static readonly Color color_DM_Other;

	private void Start()
	{
	}

	private void Update()
	{
	}

	public void DeathEvent(DeathEventData data)
	{
	}

	public static void NanoInfect(string nanoName, string soldierName, Sprite icon)
	{
	}

	public void AddMsg(string killerName, Color killerColor, string deadName, Color deadColor, Sprite icon, bool isVVIP, HeadShotType headShot, bool wallThrough, SpecialKillType specialKill, NanoKillType nanoKill, int multiKill)
	{
	}

	private HUD_KillMsgIndividual GetMsg()
	{
		return null;
	}

	private Color GetColor(Player player)
	{
		return default;
	}
}
