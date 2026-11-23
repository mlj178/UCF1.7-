using UnityEngine;

public class WPN_StunGrenade2 : MonoBehaviour
{
	[SerializeField]
	private GameObject stunBuffEffect;

	[SerializeField]
	private GameObject screenFX;

	private void Awake()
	{
	}

	private void OnCauseDamage(Entity victim)
	{
	}
}
