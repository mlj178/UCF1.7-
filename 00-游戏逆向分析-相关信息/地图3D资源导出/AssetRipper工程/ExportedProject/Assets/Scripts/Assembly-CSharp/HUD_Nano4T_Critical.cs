using UnityEngine;

public class HUD_Nano4T_Critical : MonoBehaviour
{
	[SerializeField]
	private GameObject textPrefab;

	private SimpleObjectPool pool;

	private void Awake()
	{
	}

	private void GameManager_MyPlayerCasueDamageEvent_Observers(ref DamageEventData data)
	{
	}

	private void ShowDamage(int damage)
	{
	}
}
