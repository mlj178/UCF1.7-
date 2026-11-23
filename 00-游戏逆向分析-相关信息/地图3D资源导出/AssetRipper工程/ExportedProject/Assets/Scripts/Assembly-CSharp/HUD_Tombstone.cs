using UnityEngine;
using UnityEngine.UI;

public class HUD_Tombstone : Singleton<HUD_Tombstone>
{
	[SerializeField]
	private GameObject otherBarPrefab;

	[SerializeField]
	private Text tip;

	[SerializeField]
	private Image bar;

	[SerializeField]
	private Text hpText;

	private HealthData myTombHealth;

	private void Update()
	{
	}

	public static HUD_HealthBar AddHealthBar(TombStone tomb)
	{
		return null;
	}

	public void BindMyTomb(RecyclableObject tombRO, HealthData health)
	{
	}

	private void OnMyTombRecycle()
	{
	}

	private void ShowRespawnTip()
	{
	}

	public static void StopRespawnCountDown()
	{
	}

	private void OnMyPlayerRespawn(Player myPlayer)
	{
	}
}
