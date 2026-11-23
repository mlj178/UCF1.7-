using System;

public class WPN_SentryGun : Weapon
{
	private WD_SentryGun realData;

	private WPN_Gun.AmmoData ammo;

	public Action<SentryGun> SetSuccess_Listener;

	public Func<bool> SetCheck_Listener;

	public override void Init()
	{
	}

	protected override void OnGenerateFromOwner()
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	protected override void Update()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	public void TrySet()
	{
	}

	private void SetSentryGun()
	{
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}

	public override void BotControl(Bot bot)
	{
	}
}
