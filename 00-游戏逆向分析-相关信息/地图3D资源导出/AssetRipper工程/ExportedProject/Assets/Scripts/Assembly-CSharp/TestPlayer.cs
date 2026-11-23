using Pathfinding;
using UnityEngine;

public class TestPlayer : MonoBehaviour
{
	public Transform destination;

	public Transform aim;

	public Transform escape;

	private Seeker seeker;

	private float nextRepathTime;

	private void Awake()
	{
	}

	private void Update()
	{
	}

	private void OnPathComplete(Path newPath)
	{
	}
}
