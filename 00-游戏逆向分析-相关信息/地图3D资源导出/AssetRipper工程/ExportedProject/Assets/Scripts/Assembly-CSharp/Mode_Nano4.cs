using UnityEngine;

public class Mode_Nano4 : ModeBase_Nano
{
	private static readonly Vector2 supplyArriveTip_Pos;

	private static readonly Vector2 supplyGetTip_Pos;

	[SerializeField]
	private CommonHud_1 terminatorMsg;

	[SerializeField]
	private CommonHud_1 characterMark;

	[SerializeField]
	private HUD_Nano4_HumanGauge humanGauge;

	[SerializeField]
	private CommonHud_1 becomeHeroKeyTip;

	private static Vector2 heroKeyTip_Pos;

	private static readonly int[] heroNeedDeadSoldier;

	[SerializeField]
	private bool isVariant;

	public static Mode_Nano4 instance3 { get; private set; }

	public static bool isHeroReady => false;

	protected override void Awake()
	{
	}

	protected override void OnDestroy()
	{
	}

	private void OnNewPlayerJoin(Player player)
	{
	}

	protected override void OnStartNewGameRound()
	{
	}

	protected override void GenerateNanoGhost()
	{
	}

	protected virtual int GetHeroAppearNeedDeadSoldierCount()
	{
		return 0;
	}

	private void GenerateTerminator()
	{
	}

	protected virtual int GetTerminatorCount()
	{
		return 0;
	}

	protected virtual NanoRole GetBornTerminatorRole()
	{
		return NanoRole.Soldier;
	}

	protected override void InfectEvent(Player nanoGhost, Player soldier)
	{
	}

	protected void TryAddDeadSoldierCount()
	{
	}

	protected virtual NanoRole GetHeroRole(Player player)
	{
		return NanoRole.Soldier;
	}

	protected override float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag damageTag, int attackerLevel)
	{
		return 0f;
	}

	private void TryBecomeHero(Player player, KeyInputState inputState)
	{
	}

	public void BecomeHero(Player player, NanoRole role, bool textTip)
	{
	}

	public void BecomeMasterTerminator(Player player, NanoRole role, bool textTip)
	{
	}

	protected void AddHeroRadarIcon(Player player)
	{
	}

	private void ShowTerminatorMsg(string msg)
	{
	}

	protected override void ShowTip_GetSupply(string msg)
	{
	}

	protected override void ShowTip_SupplyBoxArrive(string msg)
	{
	}

	protected override void ShowTip_GetSkill()
	{
	}

	private void DamageEvent(ref DamageEventData data)
	{
	}

	private void DeathEvent(DeathEventData eventData)
	{
	}

	protected virtual void AddExtraKillScore(Player killer, Player dead)
	{
	}

	private void PlayHeroDieSnd(NanoRole role)
	{
	}

	protected override void AddInfectScore(Player nanoGhost, Player soldier)
	{
	}

	protected override void AddSoldierWinScore()
	{
	}
}
