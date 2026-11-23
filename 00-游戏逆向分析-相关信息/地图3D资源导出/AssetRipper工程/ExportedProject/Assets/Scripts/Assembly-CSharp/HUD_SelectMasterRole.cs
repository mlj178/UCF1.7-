using UnityEngine;
using UnityEngine.UI;

public class HUD_SelectMasterRole : MonoBehaviour
{
	private Image img;

	[SerializeField]
	private Sprite[] sprs;

	private NanoRoleSelect roleSelect;

	private void Awake()
	{
	}

	private void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)
	{
	}

	private void PlayerController_FocusHUD_Listenner(ref string hud)
	{
	}

	private void NanoRoleSelect_Type_Listnner(NanoRoleSelect.Type obj)
	{
	}
}
