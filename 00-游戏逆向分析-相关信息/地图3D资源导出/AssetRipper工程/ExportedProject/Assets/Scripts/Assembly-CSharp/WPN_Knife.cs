using System;

public class WPN_Knife : Weapon
{
	[Serializable]
	public enum KnifeAttackType
	{
		None = 0,
		Combo1 = 1,
		Combo2 = 2,
		Bigshot = 3,
		Other = 4
	}

	private float combo1_AnimSpeed;

	protected static readonly string AnimTag_KnifeAttack;

	protected WeaponData_Knife realData => null;

	public override void Init()
	{
	}

	protected override void Update()
	{
	}

	public override void OnSpecialBtnDown()
	{
	}

	protected virtual void PlayKnifeAttackAnim(KnifeAttackType type)
	{
	}

	public override void AnimSpeedSetting()
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	protected virtual void OnKnifeAttackAnimEnd(string animName)
	{
	}

	protected void KnifeAttackEvent(int index)
	{
	}

	protected override KnifeAttackData GetKnifeAttackData(int attackIndex)
	{
		return default;
	}

	protected override string GetKnifeHitSoundName(int attackIndex)
	{
		return null;
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}

	public override void BotControl(Bot bot)
	{
	}
}
