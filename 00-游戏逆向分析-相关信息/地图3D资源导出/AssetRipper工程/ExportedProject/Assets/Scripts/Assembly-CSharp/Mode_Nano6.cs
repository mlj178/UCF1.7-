using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Mode_Nano6 : ModeBase_Nano
{
	public struct RadioMsg
	{
		public AudioClip audio;

		public string message;

		public string attachMark;
	}

	private Nano6ModeAsset realAsset;

	[SerializeField]
	private CommonHud_1 eventTip;

	[SerializeField]
	private CommonHud_1 levelUpTip;

	[SerializeField]
	private CommonHud_1[] levelUpText;

	private Coroutine levelUpTextDraCoroutine;

	[SerializeField]
	private GameObject thermalVisionIcon;

	[SerializeField]
	private CommonHud_1 skillTip;

	[SerializeField]
	private Image nanoClothCount;

	[SerializeField]
	private HUD_ProjectionSign oneshineSign;

	public static Action<float, float> soldierExp_Listener;

	private AudioSource radio;

	private List<RadioMsg> radioPlayList;

	private bool firstWaveSupplyBox;

	private bool firstInfect;

	private bool firstMeleeKillNano;

	private bool ghostBladeWillAppearTip;

	private SimpleObjectPool buffIconPool;

	[SerializeField]
	private GameObject buffIconPrefab;

	[SerializeField]
	private Transform[] buffIconTargets;

	private const int Score_NanoWin = 100;

	private const int Score_Infect = 200;

	private const int Score_NanoHookItem = 100;

	private const int Score_DamageGhostBlade = 100;

	private const int Score_KillGhostBlade = 100;

	private const int Score_NanoDeath = 50;

	private const int Score_SoldierWin = 200;

	private const int Score_KillNano = 200;

	private const int Score_SecKillNano = 300;

	private const int Exp_Infect = 10;

	private const int Exp_InfectFailed = 5;

	private const int Exp_DamageGhostBlade = 3;

	public static readonly int[] soldierLevelUpNeedExp;

	public static Mode_Nano6 instance3 => null;

	public float soldierExp { get; private set; }

	public int soldierLevel { get; private set; }

	protected override void Awake()
	{
	}

	protected override void Update()
	{
	}

	protected override void OnDestroy()
	{
	}

	protected override void OnMyPlayerJoin(Player myPlayer)
	{
	}

	protected override void InitSetting()
	{
	}

	protected override void SetBornNanoGhostHP(Player player, NanoRole role)
	{
	}

	protected override void InvalidDmgCheck(ref DamageEventData eventData)
	{
	}

	protected override void InfectEvent(Player nanoGhost, Player soldier)
	{
	}

	protected override void ShowTip_Infected()
	{
	}

	protected override void AddInfectExp(Player nanoGhost)
	{
	}

	protected override void SetInfectedHP(Player nanoGhost, Player soldier)
	{
	}

	protected override void AddInfectScore(Player nanoGhost, Player soldier)
	{
	}

	protected override void PostDamageEvent(ref DamageEventData eventData)
	{
	}

	private void DeathEvent(DeathEventData eventData)
	{
	}

	protected override bool GetShouldResetDeadNanoGhostExp(Player player)
	{
		return false;
	}

	protected override void OnStartNewGameRound()
	{
	}

	protected override void StartGenerateSupplyBox()
	{
	}

	protected override void ShowTip_NanoAppear()
	{
	}

	private void OnMyPlayerBecomeNanoGhost(NanoRole oldRole, NanoRole newRole)
	{
	}

	protected override void OnSupplyBoxArrive()
	{
	}

	protected override void ShowTip_SupplyBoxArrive(string msg)
	{
	}

	protected override void ShowTip_GetSupply(string msg)
	{
	}

	private void SetSoldierExp(float exp)
	{
	}

	private void SoldierLevelUp()
	{
	}

	private void AddSoldierMainWpnAmmo(int count)
	{
	}

	public static bool BecomeGhostBlade(Player player)
	{
		return false;
	}

	protected override void NanoGhostLevelUp(Player player)
	{
	}

	public bool BecomeArmoredTerminator(Player player)
	{
		return false;
	}

	private void SetNanoGhostHP(Player player)
	{
	}

	protected override void AddNanoGhostItemBonusHP(Player player)
	{
	}

	private void DrawLevelUpText(Nano6ModeAsset.UpgradeAsset upgradeAsset)
	{
	}

	protected override float CalKnifeDmg(NanoRole attackerRole, float baseDmg, DamageTag dmgTag, int attackerLevel)
	{
		return 0f;
	}

	public void ThermalVisionSetting()
	{
	}

	public override void SetNanoClothUI(int count)
	{
	}

	public override void OnPlayerPickUpSupplyBox(Player player, SupplyBox.Type boxType)
	{
	}

	private void AddRadioMsg(AudioClip audio, string msg, string attachMark)
	{
	}

	private void RadioPlaying()
	{
	}

	protected override void GhostWin()
	{
	}

	protected override void AddGhostWinScore()
	{
	}

	protected override void SoldierWin()
	{
	}

	protected override void AddSoldierWinScore()
	{
	}

	public static string NumLerpAnim(int num, float duration)
	{
		return null;
	}

	public static void SetOneShineTarget(Transform target)
	{
	}

	protected override int GetSkillHPcost(Player player)
	{
		return 0;
	}
}
