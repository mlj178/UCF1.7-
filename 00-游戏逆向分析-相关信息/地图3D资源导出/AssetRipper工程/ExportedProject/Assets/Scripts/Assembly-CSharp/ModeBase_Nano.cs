using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ModeBase_Nano : ModeBase
{
	public NanoModeAsset asset;

	public NanoModeBasicAsset basicAsset;

	[SerializeField]
	protected CommonHud_1 nanoTimerTip;

	[SerializeField]
	protected HUD_Nano_FinalBattle finalBattle;

	[SerializeField]
	protected CommonHud_1 hpRecoverIcon;

	[SerializeField]
	protected CommonHud_1 gKeyTip;

	[SerializeField]
	protected CommonKillMark mark;

	[SerializeField]
	protected GameObject nanoClothIcon;

	[SerializeField]
	protected CommonHud_1 supplyBoxTip;

	[SerializeField]
	protected CommonHud_1 meleeKillNanoTip;

	[SerializeField]
	private AnimationHud nanoKillMark;

	[SerializeField]
	private AnimationHud nanoKillMark_MultiKill;

	protected int thisRoundPlayer;

	public static int soldierAttackPower;

	protected List<int> ignoreSoldierPowerWpnList;

	private List<Player> respawningPlayer;

	protected NameKeyPool supplyBoxPool;

	protected List<Player> randomPlayerList;

	public static int[] nanoLevelUpNeedExp;

	protected static int BornNanoGhostHP;

	protected static float AbsorbNeedTime;

	protected static int AbsorbCheckCount;

	protected static readonly string Text_GetSkill;

	protected static readonly string[] Tip_Infect;

	public static ModeBase_Nano instance2 => null;

	public static bool nanoRespawn_Melee { get; private set; }

	public static bool nanoRespawn_Headshot { get; private set; }

	public static int maxLevel => 0;

	protected override void Awake()
	{
	}

	protected override void ScoreBoardTexSetting()
	{
	}

	protected override void OnStartNewGameRound()
	{
	}

	protected int GetNanoAppearTime()
	{
		return 0;
	}

	private IEnumerator NanoTimer()
	{
		return null;
	}

	protected virtual void InitSetting()
	{
	}

	private void UpdateRandomPlayerList()
	{
	}

	protected virtual int GetNanoGhostCount()
	{
		return 0;
	}

	protected virtual void GenerateNanoGhost()
	{
	}

	protected virtual void ShowTip_NanoAppear()
	{
	}

	protected void UpdateCharacterModel(Player player)
	{
	}

	public void UpdateNanoRole(Player player, NanoRole newRole)
	{
	}

	protected void UpdateNanoRole(Player player)
	{
	}

	protected void CalBornNanoGhostHP()
	{
	}

	protected virtual void SetBornNanoGhostHP(Player player, NanoRole role)
	{
	}

	protected void PlayChangeFX(Player player)
	{
	}

	public virtual void BecomeSoldider(Player player, bool isRoundReset = true)
	{
	}

	private void DeathEvent(DeathEventData eventData)
	{
	}

	protected virtual void RespawnPlayer(Player dead, int respawnTime, bool isNormalRespawn, bool clearExp)
	{
	}

	protected virtual void SpawnEvent(Player player)
	{
	}

	protected virtual bool GetShouldResetDeadNanoGhostExp(Player player)
	{
		return false;
	}

	protected virtual void ResetNanoGhostExpAndHp(Player player)
	{
	}

	protected virtual void InvalidDmgCheck(ref DamageEventData eventData)
	{
	}

	protected virtual void PreDamageEvent(ref DamageEventData eventData)
	{
	}

	protected void PlayNanoClothMark(Texture markTex)
	{
	}

	protected virtual void PostDamageEvent(ref DamageEventData eventData)
	{
	}

	protected virtual float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag damageTag, int attackerLevel)
	{
		return 0f;
	}

	protected virtual void InfectEvent(Player nanoGhost, Player soldier)
	{
	}

	protected virtual void ShowTip_Infected()
	{
	}

	protected virtual void AddInfectScore(Player nanoGhost, Player soldier)
	{
	}

	protected virtual void SetInfectedHP(Player nanoGhost, Player soldier)
	{
	}

	protected virtual void AddInfectExp(Player nanoGhost)
	{
	}

	protected virtual void CheckRoundOver()
	{
	}

	protected override void OnTimeOut()
	{
	}

	protected virtual void SoldierWin()
	{
	}

	protected virtual void AddSoldierWinScore()
	{
	}

	protected virtual void GhostWin()
	{
	}

	protected virtual void AddGhostWinScore()
	{
	}

	protected virtual void StartGenerateSupplyBox()
	{
	}

	protected void GenerateSupplyBox(int count)
	{
	}

	protected virtual void OnSupplyBoxArrive()
	{
	}

	protected void AddNanoGhostExp(Player player, int addValue)
	{
	}

	protected void SetNanoGhostExp(Player player, int exp)
	{
	}

	protected virtual void NanoGhostLevelUp(Player player)
	{
	}

	protected virtual void GiveLevelUpBonusHp(Player player)
	{
	}

	protected void PlayAppearSound(NanoRole role)
	{
	}

	protected virtual void SetSkill(Player player)
	{
	}

	protected virtual void RemoveSkill(Player player, NanoRole oldRole)
	{
	}

	public static bool TryUseSkill(Player player)
	{
		return false;
	}

	protected virtual int GetSkillHPcost(Player player)
	{
		return 0;
	}

	protected virtual float ModifyNanoSkillColdTime(float input)
	{
		return 0f;
	}

	public bool NanoGhostSkill(Player player)
	{
		return false;
	}

	public bool NurseSkill(Player player)
	{
		return false;
	}

	public bool TerminatorSkill(Player player)
	{
		return false;
	}

	public bool DemonTerminatorSkill(Player player)
	{
		return false;
	}

	private void PlaySkillSND(NanoRole nanoRole)
	{
	}

	protected virtual void ShowTip_GetSkill()
	{
	}

	public void PlayHpRecoverFX(CharacterModel.Sex sex)
	{
	}

	public virtual void SetNanoClothUI(int count)
	{
	}

	public virtual void OnPlayerPickUpSupplyBox(Player player, SupplyBox.Type boxType)
	{
	}

	protected bool CheckNanoClothMax(Player player)
	{
		return false;
	}

	protected virtual void ShowTip_SupplyBoxArrive(string msg)
	{
	}

	protected virtual void ShowTip_GetSupply(string msg)
	{
	}

	protected void ShowTip_MeleeKillNano(string msg)
	{
	}

	protected void ShowTip_HeroReady(string msg)
	{
	}

	protected void ShowTip_HpNotEnough()
	{
	}

	protected void ShowSupplyBoxTip(string msg)
	{
	}

	protected void ShowNanoTimerTip(string msg)
	{
	}

	protected void ShowMeleeKillNanoTip(string msg)
	{
	}

	private void KillMarkEvent(ref HUD_KillMark.EventData evtData)
	{
	}

	private void DrawNanoKillMark(NanoRole role, int multiKill)
	{
	}

	protected void AddSign(Player player)
	{
	}

	private void OnNewPlayerJoin(Player newPlayer)
	{
	}

	private void AddAbsorbFuction(Player newPlayer)
	{
	}

	private void AbsorbFunction(Player player, KeyInputState keyState)
	{
	}

	public void ChangeNanoGhostType(Player player, NanoRole role)
	{
	}

	protected virtual void AddNanoGhostItemBonusHP(Player player)
	{
	}
}
