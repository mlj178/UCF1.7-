using UnityEngine;

public class WPN_RPG : Weapon
{
	private WPN_Gun.AmmoData ammo;

	private WD_RPG realData;

	[SerializeField]
	private ParticleSystem gunfire;

	private WPN_Gun.SemiGunFireLinkState fireState;

	public override void Init()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	protected override void OnGenerateFromOwner()
	{
	}

	public override void CrosshairSetting()
	{
	}

	public override void AnimSpeedSetting()
	{
	}

	public override void OnFireBtnPressed()
	{
	}

	protected override void Update()
	{
	}

	public override void OnFireBtnUnPressed()
	{
	}

	protected void Fire()
	{
	}

	public override void OnReloadBtnDown()
	{
	}

	public bool CanReload()
	{
		return false;
	}

	protected void Reload()
	{
	}

	protected void ReloadOver()
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	public override void BotControl(Bot bot)
	{
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}

	public void FillAmmo()
	{
	}
}
