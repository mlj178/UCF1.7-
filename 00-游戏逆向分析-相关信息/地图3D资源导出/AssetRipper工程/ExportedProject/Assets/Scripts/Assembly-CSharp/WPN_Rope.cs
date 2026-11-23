using UnityEngine;

public class WPN_Rope : Weapon
{
	[SerializeField]
	private GameObject scrFX;

	private float deltaY;

	private Vector3 startPoint;

	private Vector3 endPoint;

	private float readyNeedTime;

	private float readyDuration;

	private float slideStartTime;

	private float slideNeedTime;

	private float slideEndTime;

	private float slideSpeed;

	private bool slideStarted => false;

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	protected override void OnAnimationEnd(string animName, string animTag)
	{
	}

	private void CalculateReadyData()
	{
	}

	protected override void Update()
	{
	}

	public override void UnDeploy(bool temporary = false)
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	private void RopeStart()
	{
	}

	private void RopeEnd()
	{
	}

	public void SetPoint(Vector3 start, Vector3 end)
	{
	}

	public bool GetNextPos(out Vector3 nextPos)
	{
		nextPos = default;
		return false;
	}
}
