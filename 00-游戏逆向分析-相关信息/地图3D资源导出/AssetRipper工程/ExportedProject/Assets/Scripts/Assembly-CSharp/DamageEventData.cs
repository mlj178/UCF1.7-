using UnityEngine;

public struct DamageEventData
{
	public Entity attacker;

	public Entity victim;

	public float damage;

	public Vector3 origin;

	public Vector3 hitPos;

	public string hitTag;

	public string hitSndName;

	public string hitEffect;

	public bool wallThrough;

	public DamageType type;

	public DamageTag damageTag;

	public int wpnIndex;

	public int wpnSprIndex;

	public bool ignoreDmgRate;

	public Sprite killMsgIcon => null;

	public void TakePlace()
	{
	}

	public void Print()
	{
	}
}
