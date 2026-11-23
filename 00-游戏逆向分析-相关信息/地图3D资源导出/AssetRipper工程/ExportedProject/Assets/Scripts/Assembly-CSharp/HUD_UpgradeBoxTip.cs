using UnityEngine;
using UnityEngine.UI;

public class HUD_UpgradeBoxTip : MonoBehaviour
{
	private GameObject background;

	private Text text;

	private Team tipTeam;

	private float arriveTime;

	private float closeTime;

	private void Awake()
	{
	}

	private void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)
	{
	}

	private void MyPlayer_team_Listenner(Team team)
	{
	}

	private void Update()
	{
	}

	public void Show(float arriveTime, Team tipTeam)
	{
	}

	public void Close()
	{
	}

	private void UpdateText()
	{
	}
}
