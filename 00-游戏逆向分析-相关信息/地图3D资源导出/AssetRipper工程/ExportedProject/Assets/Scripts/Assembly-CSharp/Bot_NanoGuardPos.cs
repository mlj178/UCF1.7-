using UnityEngine;

public class Bot_NanoGuardPos : MonoBehaviour
{
	[SerializeField]
	private Vector3[] zoomPos;

	private float nextRandomTime;

	private int lastZoomPosIndex;

	[SerializeField]
	private int _safety;

	public Bot_NanoGuardArea area { get; private set; }

	public int safety => 0;

	public void Init(Bot_NanoGuardArea area)
	{
	}

	public void Leave()
	{
	}

	private void OnDrawGizmosSelected()
	{
	}

	public Vector3 GetRandomZoomPos()
	{
		return default;
	}

	private void OnDrawGizmos()
	{
	}
}
