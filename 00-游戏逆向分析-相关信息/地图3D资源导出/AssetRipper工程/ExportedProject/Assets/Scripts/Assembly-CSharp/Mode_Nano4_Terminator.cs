using System.Collections.Generic;
using UnityEngine;

public class Mode_Nano4_Terminator : Mode_Nano4
{
	private Nano4TerminatorModeAsset realAsset;

	[SerializeField]
	private HUD_UpgradeBoxTip upgradeBoxTip;

	[SerializeField]
	private CommonHud_1 nanoItemTip;

	[SerializeField]
	private Nano4T_AttributeAsset attributeAsset;

	[SerializeField]
	private HUD_Nano4T_Attribute hud_Attribute;

	public Nano4T_Attribute attribute_Nano;

	public Nano4T_Attribute attribute_Human;

	public static bool isAttributeEnable;

	public static bool isBattleRound;

	public static bool isBattleStart;

	private SimpleObjectPool tombstonePool;

	private bool getSpecialWpn;

	private List<int> ignoreDmgBuffWeapon;

	private static readonly int[] heroNeedDeadSoldier_30;

	private static readonly int[] upgradeBoxCount;

	private bool nextNormalTerminator;

	protected override void Awake()
	{
	}

	protected override void OnDestroy()
	{
	}

	protected override void InitSetting()
	{
	}

	protected override int GetHeroAppearNeedDeadSoldierCount()
	{
		return 0;
	}

	protected override int GetTerminatorCount()
	{
		return 0;
	}

	protected override int GetNanoGhostCount()
	{
		return 0;
	}

	protected override NanoRole GetBornTerminatorRole()
	{
		return NanoRole.Soldier;
	}

	protected override bool GetShouldResetDeadNanoGhostExp(Player player)
	{
		return false;
	}

	protected override void OnSupplyBoxArrive()
	{
	}

	public override void OnPlayerPickUpSupplyBox(Player player, SupplyBox.Type boxType)
	{
	}

	protected override float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag damageTag, int attackerLevel)
	{
		return 0f;
	}

	protected override void OnStartNewGameRound()
	{
	}

	public override void BecomeSoldider(Player player, bool isRoundReset = true)
	{
	}

	protected override void GenerateNanoGhost()
	{
	}

	protected override void ShowTip_NanoAppear()
	{
	}

	protected override void StartGenerateSupplyBox()
	{
	}

	private void BecomeRandomMasterHero(Player target, bool deadToTerminator)
	{
	}

	private void TryBecomeRandomMasterTerminator(Player target)
	{
	}

	protected override NanoRole GetHeroRole(Player player)
	{
		return NanoRole.Soldier;
	}

	protected override void SetBornNanoGhostHP(Player player, NanoRole role)
	{
	}

	protected override void GiveLevelUpBonusHp(Player player)
	{
	}

	protected override void AddNanoGhostItemBonusHP(Player player)
	{
	}

	protected override int GetSkillHPcost(Player player)
	{
		return 0;
	}

	private void DamageEvent(ref DamageEventData evtData)
	{
	}

	private void DeathEvent(DeathEventData evtData)
	{
	}

	protected override void SpawnEvent(Player player)
	{
	}

	protected override void InfectEvent(Player nanoGhost, Player soldier)
	{
	}

	protected override void AddInfectScore(Player nanoGhost, Player soldier)
	{
	}

	protected override void AddExtraKillScore(Player killer, Player dead)
	{
	}

	protected override float ModifyNanoSkillColdTime(float input)
	{
		return 0f;
	}

	private void AddInfectExpLayer(Player player)
	{
	}

	private bool CheckHumanDamageBuff(int wpnID, DamageTag dmgTag, DamageType dmgType)
	{
		return false;
	}

	private bool CheckKillNanoBuff(int wpnID, DamageTag dmgTag, DamageType dmgType)
	{
		return false;
	}

	private bool CheckCriticalBuff(int wpnID, DamageTag dmgTag, DamageType dmgType)
	{
		return false;
	}

	public void BecomeSavior(Player player)
	{
	}

	protected override void RemoveSkill(Player player, NanoRole oldRole)
	{
	}

	protected override void SetSkill(Player player)
	{
	}

	private void AddPropertyModifier(Player newPlayer)
	{
	}

	private void RapidReload(Player player, ref float speed)
	{
	}

	private void NailExtraRange(Player player, ref float range)
	{
	}

	private void OnGetGrenadeFromBag(Weapon wpn)
	{
	}

	private void HotKnifeSpeed(Player player, ref float speed)
	{
	}

	private void MoveSpeedModifier(Player player, ref float speed)
	{
	}

	protected override void RespawnPlayer(Player dead, int respawnTime, bool isNormalRespawn, bool clearExp)
	{
	}
}
