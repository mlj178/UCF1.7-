using System.Collections.Generic;
using UnityEngine;

public class WPN_GhostBlade : WPN_Knife
{
	private WD_GhostBlade data2;

	private const float secKillHp = 550f;

	private const float secKillDot = 0.5f;

	private const float secKillRange = 5f;

	public static readonly string secKillhitTag;

	private List<Player> secKillTargets;

	private Player killTarget;

	private const float dashSpeed = 10f;

	private const float dashTime = 0.3f;

	[SerializeField]
	private ParticleSystem defenseFX;

	private Skill_ModeChange skill;

	public bool defense { get; private set; }

	public override void Init()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	protected override void ResetModeChange()
	{
	}

	protected override void SetValidOwner()
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	protected override void Update()
	{
	}

	protected override void UpdateDisabledSetting(PlayerWeapons wpns)
	{
	}

	private bool CanSecKill(Player player)
	{
		return false;
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	private void OnSecKillAnimEnd()
	{
	}

	public override CharWpnAnimData GetCharWpnAnimData()
	{
		return default;
	}

	protected override void PlayKnifeAttackAnim(KnifeAttackType type)
	{
	}

	public bool TryChangeMode()
	{
		return false;
	}

	public override void OnSpecialBtnDown()
	{
	}

	public override void OnSpecialBtnPressed()
	{
	}

	public override void OnSpecialBtnUnPressed()
	{
	}

	public override void OnJumpBtnDown()
	{
	}

	private void InvalidDmgCheck(ref DamageEventData eventData)
	{
	}

	public override string GetWpnName()
	{
		return null;
	}
}
