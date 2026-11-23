using UnityEngine;

public class LockVelocityArea : MonoBehaviour
{
	[SerializeField]
	private float speed;

	[SerializeField]
	private float lockTime;

	[SerializeField]
	private bool saveVelY;

	private void OnTriggerStay(Collider other)
	{
	}
}
