public class WPN_Arcane : Weapon
{
	private WD_Missile realData => null;

	public override void Init()
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	private void Throw()
	{
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}
}
