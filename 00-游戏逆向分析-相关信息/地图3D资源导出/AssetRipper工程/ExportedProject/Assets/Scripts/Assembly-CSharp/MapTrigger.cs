using UnityEngine;

public class MapTrigger : MonoBehaviour
{
	[SerializeField]
	protected Sprite tipSprite;

	[SerializeField]
	protected GameObject bindGauge;

	[SerializeField]
	protected float interactNeedTime;

	[SerializeField]
	protected bool posChangeBreak;

	private void OnTriggerStay(Collider other)
	{
	}

	protected virtual void OnPlayerStay(Player player)
	{
	}

	private void OnTriggerExit(Collider other)
	{
	}

	public virtual void OnPlayerExit(Player player)
	{
	}

	public virtual void Active(Player player)
	{
	}

	public bool CanBeInteractor(Player player)
	{
		return false;
	}

	public virtual bool CanInteract()
	{
		return false;
	}

	public virtual void StartInteract(Player player)
	{
	}

	protected virtual Sprite GetTipSprite()
	{
		return null;
	}
}
