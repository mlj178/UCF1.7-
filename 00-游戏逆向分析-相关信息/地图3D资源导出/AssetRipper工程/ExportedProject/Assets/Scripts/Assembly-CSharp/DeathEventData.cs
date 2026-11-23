using UnityEngine;

public struct DeathEventData
{
	public Entity killer;

	public Entity dead;

	public HeadShotType headShot;

	public bool wallThrough;

	public DamageType damageType;

	public Vector3 damageOrigin;

	public SpecialKillType specialKill;

	public NanoKillType nanoKill;

	public bool revenge;

	public DamageTag damageTag;

	public int wpnIndex;

	public int wpnSprIndex;

	public Sprite killMsgIcon => null;

	public bool isVVIP => false;

	public string wpnName => null;
}
