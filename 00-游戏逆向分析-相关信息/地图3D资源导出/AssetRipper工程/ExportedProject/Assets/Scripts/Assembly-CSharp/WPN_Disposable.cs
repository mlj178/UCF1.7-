public class WPN_Disposable : Weapon
{
	protected override void Update()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	public override void AnimSpeedSetting()
	{
	}

	private void OnAnimExit()
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
