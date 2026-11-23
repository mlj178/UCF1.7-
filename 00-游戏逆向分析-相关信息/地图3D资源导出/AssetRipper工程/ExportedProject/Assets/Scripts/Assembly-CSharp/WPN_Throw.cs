using UnityEngine;

public class WPN_Throw : Weapon
{
	public static readonly Vector3 throwOffset;

	private WD_Missile realData;

	private WPN_Gun.AmmoData ammoData;

	private bool throwReady;

	public override void Init()
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	protected override void Update()
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	protected override void OnGenerateFromOwner()
	{
	}

	private void Throw()
	{
	}

	private void OnFireAnimEnd()
	{
	}

	private void Reload()
	{
	}

	public override bool GiveUp(bool death = true)
	{
		return false;
	}

	public void Set5Times()
	{
	}
}
