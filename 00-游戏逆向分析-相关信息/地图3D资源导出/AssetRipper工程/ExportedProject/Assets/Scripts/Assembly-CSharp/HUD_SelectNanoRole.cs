using UnityEngine;
using UnityEngine.UI;

public class HUD_SelectNanoRole : MonoBehaviour
{
	[SerializeField]
	private GameObject main;

	[SerializeField]
	private GameObject[] images;

	[SerializeField]
	private Text timeText;

	private NanoRoleSelect roleSelect;

	private void Awake()
	{
	}

	private void PlayerController_FocusHUD_Listenner(ref string hud)
	{
	}

	private void Update()
	{
	}

	private void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)
	{
	}

	private void NanoRoleSelect_Type_Listnner(NanoRoleSelect.Type obj)
	{
	}

	private void UpdateTimeText()
	{
	}
}
