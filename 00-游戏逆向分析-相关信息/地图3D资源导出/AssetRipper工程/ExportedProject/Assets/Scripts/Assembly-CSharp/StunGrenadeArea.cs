using UnityEngine;

public class StunGrenadeArea : MonoBehaviour
{
	[SerializeField]
	private AudioClip hitSnd;

	private void Awake()
	{
	}

	private void OnTriggerStay(Collider other)
	{
	}
}
