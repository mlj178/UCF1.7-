using UnityEngine;

public class PlayerVelocity
{
	internal enum VelLockType
	{
		None = 0,
		Map = 1,
		Dash = 2
	}

	private Player owner;

	public Vector3 velocity;

	private VelLockType lockType;

	private float velUnlockTime;

	public float x => 0f;

	public float y
	{
		get
		{
			return 0f;
		}
		set
		{
		}
	}

	public float z => 0f;

	public Vector3 direction => default;

	public Vector3 horizontalDir => default;

	public bool isVelUnlock => false;

	public Vector3Int tryMoveDir { get; private set; }

	public bool isTryMoving => false;

	public bool dashOnGround { get; private set; }

	public PlayerVelocity(Player owner)
	{
	}

	public void Limit(float speed)
	{
	}

	public void ClearGravity()
	{
	}

	public void ClearVelocity()
	{
	}

	public void SetMapDash(Vector3 vel, float duration, bool isHorizontal)
	{
	}

	public void SetDash(float speed, float duration, bool dashOnGround)
	{
	}

	public void LockVelocity(float lockTime)
	{
	}

	public Vector3Int GetDashDirection()
	{
		return default;
	}

	public void Update(int x, int z)
	{
	}

	public bool ShouldMoveOnGround()
	{
		return false;
	}
}
