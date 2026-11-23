using UnityEngine;

public class HUD_NanoExpGauge : MonoBehaviour
{
	private GameObject bg;

	[SerializeField]
	private GameObject[] expObjs;

	private void Awake()
	{
	}

	private void OnMyPlayerJoin(Player myPlayer)
	{
	}

	private void OnNanoExpChange(int oldExp, int newExp)
	{
	}

	private void OnNanoRoleChange(NanoRole oldRole, NanoRole newRole)
	{
	}

	private void OnLifeStateChange(bool isAlive)
	{
	}
}
