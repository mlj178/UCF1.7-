using UnityEngine;

public class Bot_GuardPos : MonoBehaviour
{
	[SerializeField]
	protected Team team;

	[SerializeField]
	private Vector3[] zoomPos;

	private int zoomPosIndex;

	private float nextZoomPosChangeTime;

	public Player owner { get; protected set; }

	private void Update()
	{
	}

	public void SetOwner(Player newOwner)
	{
	}

	protected virtual void OnSetValidOwner()
	{
	}

	protected virtual void OnSetNullOwner()
	{
	}

	private void OnDrawGizmos()
	{
	}

	private void OnDrawGizmosSelected()
	{
	}

	public bool TryGetZoomPos(out Vector3 pos)
	{
		pos = default;
		return false;
	}
}
