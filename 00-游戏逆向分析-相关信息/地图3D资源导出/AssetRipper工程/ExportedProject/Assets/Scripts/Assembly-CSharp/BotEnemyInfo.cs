using UnityEngine;

public class BotEnemyInfo
{
	public enum DistanceControl
	{
		None = 0,
		Close = 1,
		Escape = 2
	}

	private Bot bot;

	public Entity enemy;

	public float findTime;

	public float lastLostTime;

	public Transform hitBox;

	public DistanceControl distanceControl;

	public float distanceControlChangeTime;

	public bool isClosing;

	public float nextCheckVisibleTime;

	public float lostEnemyTime => 0f;

	public bool haveEnemy => false;

	public bool isPlayer { get; private set; }

	public Vector3 enemyPos { get; private set; }

	public float distance { get; private set; }

	public Vector3 dirToEnemy { get; private set; }

	public Vector3 dirToHitBox { get; private set; }

	public float dotToHitBox => 0f;

	public BotEnemyInfo(Bot bot)
	{
	}

	public void CalGunDistanceControl(float wpnShotDistance)
	{
	}

	public void CalKnifeDistanceControl()
	{
	}

	public void Update()
	{
	}

	public bool ShouldWaitKnifeAttack()
	{
		return false;
	}
}
